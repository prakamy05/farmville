// 🌱 Indoor Farm Dashboard - React Frontend
import React, { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";

const API_URL = "http://localhost:8000";

export default function App() {
  const [data, setData] = useState([]);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/dashboard`)
      .then(res => res.json())
      .then(res => setData(res.data));

    const interval = setInterval(() => {
      fetch(`${API_URL}/dashboard`)
        .then(res => res.json())
        .then(res => setData(res.data));
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (data.length > 0) {
      const latest = data[data.length - 1];
      const currentAlerts = [];
      if (latest.soil_moisture < 25) currentAlerts.push("🚨 Low Soil Moisture");
      if (latest.temperature > 35) currentAlerts.push("🔥 High Temperature");
      if (latest.co2 > 1000) currentAlerts.push("🛑 High CO₂ Level");
      setAlerts(currentAlerts);
    }
  }, [data]);

  const zoneLatest = {};
  data.forEach(row => {
    zoneLatest[row.zone] = row;
  });

  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">🌿 Indoor Farm Dashboard</h1>

      {alerts.length > 0 && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <ul>
            {alerts.map((alert, i) => <li key={i}>{alert}</li>)}
          </ul>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {Object.entries(zoneLatest).map(([zone, d]) => (
          <div key={zone} className="bg-white rounded-xl shadow-md p-4">
            <h2 className="text-xl font-semibold mb-2">Zone {zone}</h2>
            <p>🌡️ Temp: {d.temperature} °C</p>
            <p>💧 Humidity: {d.humidity} %</p>
            <p>🪴 Soil Moisture: {d.soil_moisture} %</p>
            <p>💡 Light: {d.light} lux</p>
            <p>🍃 CO₂: {d.co2} ppm</p>
            <p className="text-sm text-gray-500">Updated: {new Date(d.timestamp).toLocaleTimeString()}</p>
          </div>
        ))}
      </div>

      <h2 className="text-2xl mt-8 mb-4 font-semibold">📈 Trends</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" tickFormatter={t => new Date(t).toLocaleTimeString()} />
          <YAxis />
          <Tooltip labelFormatter={t => new Date(t).toLocaleTimeString()} />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#e11d48" name="Temp (°C)" />
          <Line type="monotone" dataKey="soil_moisture" stroke="#059669" name="Soil Moisture (%)" />
          <Line type="monotone" dataKey="humidity" stroke="#3b82f6" name="Humidity (%)" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
