import requests
import time
import random

url = "https://你的地址.up.railway.app/event"

users = ["user1", "user2"]

devices = [
    {"type": "空调", "power_range": (800, 1500)},
    {"type": "热水器", "power_range": (1500, 3000)},
    {"type": "电饭煲", "power_range": (500, 800)}
]

while True:
    device = random.choice(devices)

    data = {
        "user_id": random.choice(users),
        "device_id": "plug_01",
        "power": random.randint(*device["power_range"]),
        "device_type": device["type"],
        "event_type": random.choice(["on", "off"])
    }

    r = requests.post(url, json=data)
    print("发送：", data)

    time.sleep(3)