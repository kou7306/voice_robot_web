from flask import Flask, redirect, request, render_template, send_from_directory,jsonify, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import asyncio
import websockets
import json
from threading import Thread
import time

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=1000000)
CORS(app, supports_credentials=True, responses={r"/*": {"origins": "*"}})
buffer_size = 20  # バッファサイズ
audio_buffer = []  # 音声データのバッファ
data_count = 0
goal_reached = False
robot_urls=["ws://100.70.4.41:5002","ws://100.112.17.4:5002"]
# "ws://100.70.4.41:5002"
# "ws://100.112.17.4:5002"

@app.route('/')
def index():
    return render_template('index.html') # templateフォルダのindex.html

@app.route('/check_goal')
def check_goal():
    global goal_reached
    return jsonify({'goal_reached': goal_reached})

@app.route('/goal_html')
def goal_html():
    return render_template('goal.html')

@app.route('/goal')
def set_goal_reached():
    print('Goal reached!')
    global goal_reached
    goal_reached = True
    return jsonify({'message': 'Goal set to reached'})

@socketio.on('connect')
def handle_connect():
    print(f'connect: {request.sid}')
    # 接続されたクライアントにメッセージを送信s


async def send_data_to_server(datas,url):  
    if datas==[]:
        data = {'volume': 0, 'frequency': 0}
    else: 
        # バッファ内のデータの平均値を計算
        volume_avg = np.mean([data['volume'] for data in datas])
        frequency_avg = np.mean([data['frequency'] for data in datas])
        data = {'volume': volume_avg, 'frequency': frequency_avg}

    async with websockets.connect(url) as websocket:        
        await websocket.send(json.dumps(data))

async def send_data_to_both_servers(audio_buffer, urls):
    tasks = []
    for url in urls:
        print(f"Sending data to {url}")
        tasks.append(send_data_to_server(audio_buffer, url))
    await asyncio.gather(*tasks)


@socketio.on('audio_data')
def handle_message(audio_data):
    global audio_buffer, data_count,goal_reached,robot_urls
    if goal_reached:
        return
    print(audio_data)

     # バッファに新しいデータを追加
    audio_buffer.append(audio_data)
    data_count += 1

    

    # バッファサイズを超えたら古いデータを削除
    if len(audio_buffer) > buffer_size:
        audio_buffer.pop(0)

    if data_count >= buffer_size:
        data_count = 0
        if(audio_data['volume'] == -1 and audio_data['frequency'] == -1):
            audio_buffer = []
        asyncio.run(send_data_to_both_servers(audio_buffer,robot_urls))

        

@app.route('/submit_url', methods=['POST'])
def submit_websocket_urls():
    try:
        global robot_urls
        data = request.get_json()
        urls = data.get('urls', [])
        # ここでURLを処理するコードを追加します
        for url in urls:
            if url != "":
                robot_urls.append(url)
        return jsonify({"message": "WebSocket URLs received successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8080)
