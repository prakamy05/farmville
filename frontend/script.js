const API_URL = "http://localhost:8000";

async function fetchData() {
  const res = await fetch(API_URL + "/dashboard");
  return await res.json();
}

function getHealthColor(score) {
  if (score >= 80) return "success";
  if (score >= 60) return "warning";
  return "danger";
}

async function renderDashboard() {
  const result = await fetchData();
  const data = result.data;
  const health = result.health;
  const latestPerZone = {};
  const alerts = [];

  data.forEach(d => latestPerZone[d.zone] = d);

  const cardsContainer = document.getElementById("cards-container");
  cardsContainer.innerHTML = "";

  Object.entries(latestPerZone).forEach(([zone, d]) => {
    const healthScore = d.health_score || 0;
    const healthColor = getHealthColor(healthScore);
    if (d.soil_moisture < 25) alerts.push(`⚠️ Low soil in ${zone}`);
    if (d.temperature > 35) alerts.push(`🔥 Temp high in ${zone}`);
    if (d.co2 > 1000) alerts.push(`🛑 CO₂ high in ${zone}`);

    cardsContainer.innerHTML += `
    <div class="col-md-6 card-zone">
      <div class="card border-${healthColor} shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Zone ${zone}</h5>
          <p>🌡️ Temp: ${d.temperature} °C | 💧 Moisture: ${d.soil_moisture}%</p>
          <p>💡 Light: ${d.light} lux | 🍃 CO₂: ${d.co2} ppm</p>
          <p>Health Score: <span class="text-${healthColor} fw-bold">${healthScore}</span></p>
          <p class="text-muted small">${new Date(d.timestamp).toLocaleTimeString()}</p>
        </div>
      </div>
    </div>`;
  });

  document.getElementById("alerts").innerHTML =
    alerts.length ? `<div class="alert alert-danger">${alerts.join("<br>")}</div>` : "";

  renderChart(data);
}

function renderChart(data) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString());
  const temperature = data.map(d => d.temperature);
  const moisture = data.map(d => d.soil_moisture);
  const humidity = data.map(d => d.humidity);

  if (window.trendChart) window.trendChart.destroy();

  window.trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        { label: "Temp (°C)", data: temperature, borderColor: "#dc3545" },
        { label: "Moisture (%)", data: moisture, borderColor: "#198754" },
        { label: "Humidity (%)", data: humidity, borderColor: "#0d6efd" }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: "top" } }
    }
  });
}

async function simulateData() {
  await fetch(API_URL + "/simulate", { method: "POST" });
  renderDashboard();
}

renderDashboard();
setInterval(renderDashboard, 15000);