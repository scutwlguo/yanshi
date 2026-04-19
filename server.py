from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# =====================
# 数据库配置（SQLite）
# =====================
DATABASE_URL = "postgresql://postgres:202420114127%40Gwl@db.xxx.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)

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
    timestamp = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

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

from fastapi.responses import HTMLResponse

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head>
        <title>用电数据管理平台</title>
        <style>
            body {
                font-family: Arial;
                background-color: #f5f7fa;
                text-align: center;
            }
            h2 {
                margin-top: 20px;
            }
            select {
                padding: 8px;
                margin: 10px;
                font-size: 16px;
            }
            table {
                border-collapse: collapse;
                margin: auto;
                width: 80%;
                background: white;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>

        <h2>🔌 用电数据可视化平台</h2>

        <label>选择用户：</label>
        <select id="user-select">
            <option value="user1">user1</option>
            <option value="user2">user2</option>
        </select>

        <table id="data-table">
            <thead>
                <tr>
                    <th>设备</th>
                    <th>状态</th>
                    <th>功率(W)</th>
                    <th>时间</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

        <script>
            async function loadData() {
                const user = document.getElementById("user-select").value;
                const res = await fetch(`/events/${user}`);
                const data = await res.json();

                const tbody = document.querySelector("#data-table tbody");
                tbody.innerHTML = "";

                data.reverse().forEach(item => {
                    const row = `
                        <tr>
                            <td>${item.device}</td>
                            <td>${item.event}</td>
                            <td>${item.power}</td>
                            <td>${item.time}</td>
                        </tr>
                    `;
                    tbody.innerHTML += row;
                });
            }

            document.getElementById("user-select").addEventListener("change", loadData);

            setInterval(loadData, 2000);
            loadData();
        </script>

    </body>
    </html>
    """