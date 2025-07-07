from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        zone TEXT,
        temperature REAL,
        humidity REAL,
        soil_moisture REAL,
        light REAL,
        co2 REAL
    )
''')
conn.commit()

class SensorData(BaseModel):
    zone: str
    temperature: float
    humidity: float
    soil_moisture: float
    light: float
    co2: float

def save_to_db(data: SensorData):
    cursor.execute("""
        INSERT INTO readings (timestamp, zone, temperature, humidity, soil_moisture, light, co2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        data.zone,
        data.temperature,
        data.humidity,
        data.soil_moisture,
        data.light,
        data.co2
    ))
    conn.commit()

@app.post("/ingest")
async def ingest(data: SensorData):
    save_to_db(data)
    return {"status": "success"}

@app.get("/dashboard")
async def dashboard():
    cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT 200")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in rows]

    health_scores = {}
    for d in data:
        score = 100
        score -= abs(25 - d["soil_moisture"]) * 1.5
        score -= abs(28 - d["temperature"]) * 1.0
        score -= abs(500 - d["co2"]) * 0.01
        d["health_score"] = max(0, min(100, round(score, 1)))
        health_scores[d["zone"]] = d["health_score"]
    return {"data": data[::-1], "health": health_scores}

@app.post("/simulate")
async def simulate():
    zones = ["A1", "A2", "B1", "B2"]
    for _ in range(6):
        data = SensorData(
            zone=random.choice(zones),
            temperature=round(random.uniform(22, 38), 2),
            humidity=round(random.uniform(45, 75), 2),
            soil_moisture=round(random.uniform(15, 55), 2),
            light=round(random.uniform(300, 900), 2),
            co2=round(random.uniform(350, 1200), 2)
        )
        save_to_db(data)
    return {"status": "simulated"}