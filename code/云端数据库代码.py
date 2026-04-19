from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

events_db = []

class Event(BaseModel):
    device_id: str
    power: float
    device_type: str
    event_type: str

@app.get("/")
def home():
    return {"msg": "server is running"}

@app.post("/event")
def receive_event(event: Event):
    data = event.dict()
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    events_db.append(data)

    print("收到事件：", data)

    return {"status": "ok"}

@app.get("/events")
def get_events():
    return events_db