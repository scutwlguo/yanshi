from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# =====================
# 数据库配置（SQLite）
# =====================
DATABASE_URL = "sqlite:///events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# =====================
# 数据库表
# =====================
class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    device_id = Column(String)
    device_type = Column(String)
    power = Column(Float)
    event_type = Column(String)
    timestamp = Column(String)

# 创建表
Base.metadata.create_all(bind=engine)

# =====================
# FastAPI
# =====================
app = FastAPI()

# =====================
# 请求模型
# =====================
class Event(BaseModel):
    user_id: str
    device_id: str
    power: float
    device_type: str
    event_type: str  # on / off

# =====================
# 首页（测试用）
# =====================
@app.get("/")
def home():
    return {"msg": "server is running"}

# =====================
# 接收事件（核心接口）
# =====================
@app.post("/event")
def receive_event(event: Event):
    db = SessionLocal()

    # ✅ 先生成时间（关键）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = EventDB(
        user_id=event.user_id,
        device_id=event.device_id,
        device_type=event.device_type,
        power=event.power,
        event_type=event.event_type,
        timestamp=timestamp
    )

    db.add(data)
    db.commit()
    db.close()

    # ✅ 用变量，不用 data.timestamp
    print(f"""
📥 新事件：
用户: {event.user_id}
设备: {event.device_type}
状态: {event.event_type}
功率: {event.power} W
时间: {timestamp}
""")

    return {"status": "ok"}

# =====================
# 查询某用户全部数据
# =====================
@app.get("/events/{user_id}")
def get_user_events(user_id: str):
    db = SessionLocal()
    data = db.query(EventDB).filter(EventDB.user_id == user_id).all()
    db.close()

    return [
        {
            "device": i.device_type,
            "power": i.power,
            "event": i.event_type,
            "time": i.timestamp
        }
        for i in data
    ]

# =====================
# 查询某用户某天数据
# =====================
@app.get("/events/{user_id}/{date}")
def get_user_events_by_date(user_id: str, date: str):
    db = SessionLocal()

    data = db.query(EventDB).filter(
        EventDB.user_id == user_id,
        EventDB.timestamp.startswith(date)
    ).all()

    db.close()

    return [
        {
            "device": i.device_type,
            "power": i.power,
            "event": i.event_type,
            "time": i.timestamp
        }
        for i in data
    ]