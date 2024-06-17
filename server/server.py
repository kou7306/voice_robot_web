import websocket
import time
import json

url = "wss://apparent-raccoon-close.ngrok-free.app/get_data"

# WebSocket接続
ws = websocket.create_connection(url)

# メッセージ送信関数
def send_message(message):
    ws.send(json.dumps(message))

# メッセージ受信関数
def receive_message():
    result = ws.recv()
    print("Received:", result)

# 定期的なリクエスト
while True:
    try:
        # リクエストを送信
        send_message({"command": "get_data"})

        # レスポンスを受信
        receive_message()

        # 10秒待機
        time.sleep()
    except KeyboardInterrupt:
        # Ctrl+Cが押されたらループを抜ける
        break

# WebSocket接続を閉じる
ws.close()
