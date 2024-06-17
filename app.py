from flask import Flask, request, render_template, send_from_directory,jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import numpy as np
import asyncio
import websockets
import json

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=1000000)
CORS(app, supports_credentials=True, responses={r"/*": {"origins": "*"}})
buffer_size = 60  # バッファサイズ
audio_buffer = []  # 音声データのバッファ

@app.route('/')
def index():
    # return send_from_directory('static', 'index.html') # staticフォルダのindex.html
    return render_template('web.html') # templateフォルダのindex.html

@socketio.on('connect')
def handle_connect():
    print(f'connect: {request.sid}')
    # 接続されたクライアントにメッセージを送信


async def send_data_to_server(data):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(data))
        message = await websocket.recv()
        print(f"Received: {message}")


@socketio.on('audio_data')
def handle_message(audio_data):
    global audio_buffer
    # バッファに新しいデータを追加
    audio_buffer.append(audio_data)
    # バッファサイズを超えたら古いデータを削除
    if len(audio_buffer) > buffer_size:
        audio_buffer.pop(0)
    
    print(audio_data)
    # 受け取ったデータを接続されている全てのクライアントにブロードキャスト
    emit('broadcast_audio_data', audio_data, broadcast=True)
       # 別のサーバーにデータを送信
    asyncio.run(send_data_to_server(audio_data))

@app.route('/get_data', methods=['GET'])
def get_data():
    global audio_buffer
    if not audio_buffer:
        return jsonify({'volume': 0, 'frequency': 0})
    # バッファ内のデータの平均値を計算
    volume_avg = np.mean([data['volume'] for data in audio_buffer])
    frequency_avg = np.mean([data['frequency'] for data in audio_buffer])
    return jsonify({'volume': volume_avg, 'frequency': frequency_avg})


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5002)
    
# ngrok http --domain=apparent-raccoon-close.ngrok-free.app 5002
