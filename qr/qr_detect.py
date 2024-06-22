import cv2
from pyzbar.pyzbar import decode
import numpy as np
import requests
import time

def detect_qr_code(image):
    decoded_objects = decode(image)
    for obj in decoded_objects:
        points = obj.polygon
        if len(points) == 4:
            pts = [(p.x, p.y) for p in points]
            cv2.polylines(image, [np.array(pts, np.int32)], True, (0, 255, 0), 2)
            qr_data = obj.data.decode('utf-8')
            cx = int((pts[0][0] + pts[2][0]) / 2)
            cy = int((pts[0][1] + pts[2][1]) / 2)
            width = np.linalg.norm(np.array(pts[0]) - np.array(pts[1]))
            return image, qr_data, width, (cx, cy)
    return image, None, None, None

def main():
    cap = cv2.VideoCapture(0)  # カメラデバイスを開く
    known_qr_code_size = 10.0  # QRコードの実際のサイズ（cm）
    focal_length = 600  # カメラの焦点距離（事前にキャリブレーションが必要）

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame, qr_data, qr_width, center = detect_qr_code(frame)

        if qr_data is not None:
            distance = (known_qr_code_size * focal_length) / qr_width
            cv2.putText(frame, f"Distance: {distance:.2f} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(f"Detected QR Code: {qr_data}, Distance: {distance:.2f} cm")

            if distance < 50:  # 例えば50cm以内
                print(qr_data)
                while True:
                    try:
                        send_get_request(qr_data)
                        break  # リクエストが成功したらループを抜ける
                    except Exception as e:
                        print(f"Failed to send request: {e}")
                        print("Retrying in {} seconds...".format(1))
                        time.sleep(1)

        cv2.imshow('QR Code Detector', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("GET request sent successfully")
    else:
        print(f"Failed to send GET request. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
