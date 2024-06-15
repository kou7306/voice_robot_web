from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, supports_credentials=True, responses={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    # return send_from_directory('static', 'index.html') # staticフォルダのindex.html
    return render_template('web.html') # templateフォルダのindex.html

@socketio.on('connect')
def handle_connect():
    print(f'connect: {request.sid}')

@socketio.on('audio_data')
def handle_message(audio_data):
    print(f'audio_data', audio_data)
    # 受け取ったデータを接続されている全てのクライアントにブロードキャスト
    emit('broadcast_audio_data', audio_data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)

