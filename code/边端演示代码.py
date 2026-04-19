import requests
import time
import random
from datetime import datetime

# 改成你的云端IP
url = "http://192.168.1.5:8000/event"

devices = [
    {"type": "空调", "power_range": (800, 1500)},
    {"type": "热水器", "power_range": (1500, 3000)},
    {"type": "电饭煲", "power_range": (500, 800)}
]

while True:
    device = random.choice(devices)

    data = {
        "device_id": "plug_01",
        "power": random.randint(*device["power_range"]),
        "device_type": device["type"],
        "event_type": random.choice(["on", "off"])
    }

    try:
        r = requests.post(url, json=data)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 已发送:", data)
    except Exception as e:
        print("发送失败：", e)

    time.sleep(3)  # 每3秒发一次