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


@app.route('/')
def index():
    # return send_from_directory('static', 'index.html') # staticフォルダのindex.html
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


async def send_data_to_server(datas,url):  
    if not datas:
        return jsonify({'volume': 0, 'frequency': 0})
    
    # バッファ内のデータの平均値を計算
    volume_avg = np.mean([data['volume'] for data in datas])
    frequency_avg = np.mean([data['frequency'] for data in datas])
    data = {'volume': volume_avg, 'frequency': frequency_avg}
    async with websockets.connect(url) as websocket:
        
        await websocket.send(json.dumps(data))

async def send_data_to_both_servers(audio_buffer):
    url2 = "ws://localhost:8765"
    url4 = "ws://100.70.4.41:5002"
    # url1 = "wss://apparent-raccoon-close.ngrok-free.app/socket.io"
    # url3= "wss://romantic-rooster-assured.ngrok-free.app/socket.io"
    await asyncio.gather(
        # send_data_to_server(audio_buffer, url1),
        send_data_to_server(audio_buffer, url2),
        send_data_to_server(audio_buffer, url4)
        # send_data_to_server(audio_buffer, url3)
    )


@socketio.on('audio_data')
def handle_message(audio_data):
    # print(f'audio_data: {audio_data}')
    global audio_buffer, data_count

     # バッファに新しいデータを追加
    audio_buffer.append(audio_data)
    data_count += 1

    

    # バッファサイズを超えたら古いデータを削除
    if len(audio_buffer) > buffer_size:
        audio_buffer.pop(0)

    # 受け取ったデータを接続されている全てのクライアントにブロードキャスト
    # emit('broadcast_audio_data', audio_data, broadcast=True)

    if data_count >= buffer_size:
        data_count = 0
        # print(audio_buffer)
        asyncio.run(send_data_to_both_servers(audio_buffer))

        



    
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8080)
    
# ngrok http --domain=apparent-raccoon-close.ngrok-free.app 5002
