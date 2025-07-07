from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI()

# CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static HTML dashboard
app.mount("/dashboard", StaticFiles(directory="frontend", html=True), name="dashboard")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

DB_TEMPLATE = os.path.join(DATA_DIR, "iot_data_%Y_%m_%d.db")


def get_db_path(timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow()
    return timestamp.strftime(DB_TEMPLATE)


def ensure_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            soil_moisture REAL,
            light_intensity REAL
        )
    """)
    conn.commit()
    conn.close()


@app.post("/ingest")
async def ingest_sensor_data(payload: dict):
    now = datetime.utcnow()
    db_path = get_db_path(now)
    ensure_db_schema(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sensor_data (timestamp, temperature, humidity, soil_moisture, light_intensity)
        VALUES (?, ?, ?, ?, ?)
    """, (
        now.isoformat(),
        payload.get("temperature"),
        payload.get("humidity"),
        payload.get("soil_moisture"),
        payload.get("light_intensity")
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/latest")
async def get_latest_data():
    db_path = get_db_path()
    if not os.path.exists(db_path):
        return JSONResponse(content={"error": "No data yet"}, status_code=404)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1", conn)
    conn.close()
    return df.to_dict(orient="records")[0] if not df.empty else {}


@app.get("/data")
async def get_historic_data(start: str, end: str):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    results = []
    curr = start_dt
    while curr <= end_dt:
        db_path = get_db_path(curr)
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            df = pd.read_sql("SELECT * FROM sensor_data", conn)
            conn.close()
            results.append(df)
        curr += timedelta(days=1)

    if results:
        full_df = pd.concat(results)
        full_df = full_df[(full_df['timestamp'] >= start) & (full_df['timestamp'] <= end)]
        return full_df.to_dict(orient="records")
    else:
        return []
