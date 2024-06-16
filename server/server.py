import requests
import time

# APIのエンドポイント
url = 'https://apparent-raccoon-close.ngrok-free.app/get_data'

# ループを使用してAPIを定期的にリクエスト
while True:
    # GETリクエストを送信
    response = requests.get(url)

    # レスポンスを取得
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print('Failed to fetch data:', response.status_code)

    # 10秒待機してから次のリクエストを送信
    time.sleep(1)
