import requests
import time

url = "https://web-production-86eb0.up.railway.app/event"

while True:
    data = {
        "user_id": "user1",
        "device_id": "plug_01",
        "power": -1200,
        "device_type": "空调",
        "event_type": "on"
    }

    res = requests.post(url, json=data)
    print(res.json())

    time.sleep(5)  # 每5秒发送一次