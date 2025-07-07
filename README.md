
# 🌿 Indoor Farm Insight Dashboard

![FastAPI](https://img.shields.io/badge/FastAPI-🚀-brightgreen)
![Chart.js](https://img.shields.io/badge/Chart.js-📈-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-Active-success)

> A sleek, real-time indoor farming dashboard built with FastAPI, SQLite, and Chart.js.

---

## 🎥 Demo

![Demo GIF](assets/Screenshot(307)...PNG)  


---

## 🚀 Features

- 📡 Real-time sensor data monitoring
- 📊 Historical data view with date range pickers
- 📈 Overlaid multi-metric chart (temperature, humidity, soil moisture, light)
- 💾 Local time-series storage in daily `.db` files
- 🧪 Sensor simulator included
- ⚡ Lightweight frontend with pure HTML + JS + Chart.js

---

## 🧠 Architecture

```
Sensor (real or simulated)
        ⬇️ POST /ingest
     [FastAPI Backend]
        ⬇️ Writes to SQLite (daily)
        ⬆️ Serves /latest + /data
     [Dashboard Frontend]
        ⬆️ Fetch + Plot with Chart.js
```

---

## 📷 Screenshots

### 🟢 Real-Time Monitoring  
![Live Data Screenshot](assets/Screenshot(307)...PNG)

### 📈 Overlay Chart  
![Overlay Chart Screenshot](assets/Screenshot(309)...PNG)

### FastAPI
![FastAPI](assets/Screenshot(311)...PNG)

### IOTSensor Simulator
![IOTSensorSimulator](assets/Screenshot(310)...PNG)

---

## 🗂️ Project Structure

```
iot-dashboard-project/
├── backend/
│   ├── main.py              ← FastAPI backend
│   └── data/                ← Daily DB files auto-created here
├── frontend/
│   └── index.html           ← Dashboard UI
├── sensor_simulator.py      ← Emulates sensor data
├── Dockerfile (optional)
└── README.md
```

---

## ⚙️ Requirements

- Python 3.8+
- Install dependencies:
  ```bash
  pip install fastapi uvicorn pandas
  ```

---

## 🛠️ Usage

### 1. Start the Backend
```bash
cd backend
uvicorn main:app --reload
```

### 2. Open the Dashboard  
[http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)

### 3. Simulate Sensor Data (optional)
```bash
python sensor_simulator.py
```

---

## 📑 API Overview

| Endpoint       | Method | Description                       |
|----------------|--------|-----------------------------------|
| `/ingest`      | POST   | Receives sensor readings          |
| `/latest`      | GET    | Most recent reading               |
| `/data`        | GET    | Readings in date range (ISO time) |

---

## 🧪 Example Sensor Payload

```json
{
  "temperature": 25.4,
  "humidity": 68.3,
  "soil_moisture": 45.2,
  "light_intensity": 1200.0
}
```

---

## 🐳 Optional: Docker Setup

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend /app
RUN pip install fastapi uvicorn pandas
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Run it
```bash
docker build -t farm-dashboard .
docker run -p 8000:8000 farm-dashboard
```

---

## ✅ Future Ideas

- [ ] CSV/Excel export for historical data
- [ ] Sensor toggles in chart
- [ ] Multi-device overlay comparison
- [ ] Mobile UI optimization
- [ ] User auth & cloud sync

---

## 👨‍🔬 Built With

- ⚡ [FastAPI](https://fastapi.tiangolo.com/)
- 📈 [Chart.js](https://www.chartjs.org/)
- 🛢️ SQLite + Pandas
- 🧠 Pure HTML & Vanilla JS

---

## 🪴 License

MIT — use freely, grow something amazing 🌱

---

### 🤝 Contribute

Have ideas? Found a bug?  
Open an issue or drop a PR!
