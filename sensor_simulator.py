import time
import requests
import random
from datetime import datetime

URL = "http://127.0.0.1:8000/ingest"

print("Starting sensor data simulator...")

while True:
    payload = {
        "temperature": round(random.normalvariate(25, 1.5), 2),
        "humidity": round(random.normalvariate(60, 8), 2),
        "soil_moisture": round(random.normalvariate(40, 4), 2),
        "light_intensity": round(random.normalvariate(500, 80), 2)
    }
    try:
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Sent: {payload}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"🚨 Connection error: {e}")

    time.sleep(10)  # Send data every 10 seconds
