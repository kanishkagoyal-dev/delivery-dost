import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import time

# =========================
# CONFIG: API base URL
# =========================
# Change this later if your API runs on a different port/host.
API_BASE = "https://delivery-dost.onrender.com"
API_V1 = API_BASE + "/api/v1"

# =========================
# PAGE SETUP
# =========================
st.set_page_config(page_title="AI Last-Mile Logistics", layout="wide")
st.title("✦ Delivery Dost")
st.markdown(
    """
    <div style="
        font-size: 20px;
        font-weight: 600;
        color: #374151;
        margin-top: -12px;
        margin-bottom: 20px;
    ">
        The brain behind every better delivery.
    </div>
    """,
    unsafe_allow_html=True,
)
# =========================
# HELPER: FETCH DATA FROM API
# =========================

def fetch_json(endpoint, default=None):
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=2)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    # Fallback default data if API is not running
    return default

# =========================
# SIDEBAR: CONTROLS
# =========================

st.sidebar.header("Controls")

if st.sidebar.button("➕ Add Order"):
    # Call API to add a dummy order (adjust endpoint as per your backend)
    try:
        requests.post(f"{API_BASE}/orders", json={
            "customer_lat": 28.62,
            "customer_lng": 77.22,
            "priority": "high",
            "items": ["Box"]
        }, timeout=2)
        st.sidebar.success("Order added (simulated).")
    except Exception:
        st.sidebar.warning("Could not reach API to add order.")

if st.sidebar.button("🚦 Simulate Traffic Jam"):
    # Tell backend to simulate traffic (adjust endpoint)
    try:
        requests.post(f"{API_BASE}/simulate/traffic_jam", timeout=2)
        st.sidebar.success("Traffic jam simulated.")
    except Exception:
        st.sidebar.warning("Could not reach API to simulate traffic.")

if st.sidebar.button("🔄 Re-optimize Now"):
    # Trigger re-optimization (adjust endpoint)
    try:
        requests.post(f"{API_BASE}/api/v1/optimize", timeout=2)
        st.sidebar.success("Re-optimization triggered.")
    except Exception:
        st.sidebar.warning("Could not reach API to re-optimize.")
st.sidebar.markdown("---")
st.sidebar.info("Auto-refresh: every 5 seconds")

# =========================
# FETCH DATA
# =========================

# 1. Deliveries: list of {lat, lng, priority, id, status, eta}
deliveries_default = [
    {"id": "D1", "lat": 28.6139, "lng": 77.2090, "priority": "high", "status": "pending", "eta": "10 mins"},
    {"id": "D2", "lat": 28.6300, "lng": 77.2200, "priority": "medium", "status": "in_transit", "eta": "20 mins"},
    {"id": "D3", "lat": 28.5900, "lng": 77.1800, "priority": "low", "status": "delivered", "eta": "-"},
]

deliveries = fetch_json("/api/v1/orders",deliveries_default)

# 2. Vehicle routes: list of {vehicle_id, color, path: [[lat, lng], ...], distance_km, cost}
routes_default = [
    {
        "vehicle_id": "V1",
        "color": "blue",
        "path": [
            [28.6139, 77.2090],
            [28.6200, 77.2150],
            [28.6300, 77.2200],
        ],
        "distance_km": 5.2,
        "cost": 120,
    },
    {
        "vehicle_id": "V2",
        "color": "red",
        "path": [
            [28.6000, 77.1900],
            [28.5950, 77.1850],
            [28.5900, 77.1800],
        ],
        "distance_km": 3.8,
        "cost": 90,
    },
]

routes = fetch_json("/api/v1/routes",
routes_default)

# 3. Road network with speeds (for traffic coloring)
# Each road: {start: [lat, lng], end: [lat, lng], speed_kmh}
roads_default = [
    {"start": [28.6100, 77.2000], "end": [28.6200, 77.2100], "speed_kmh": 40},
    {"start": [28.6200, 77.2100], "end": [28.6300, 77.2200], "speed_kmh": 15},
    {"start": [28.5900, 77.1800], "end": [28.6000, 77.1900], "speed_kmh": 35},
]

roads=fetch_json("/api/v1/traffic",roads_default)

# =========================
# COMPUTE KPIS
# =========================

total_distance = sum(r.get("distance_km", 0) for r in routes)
total_cost = sum(r.get("cost", 0) for r in routes)
vehicles_used = len(routes)

# On-time %: simple mock logic based on status
delivered_count = sum(1 for d in deliveries if d.get("status") == "delivered")
on_time_percent = round((delivered_count / max(len(deliveries), 1)) * 100)

# =========================
# DISPLAY KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Distance", f"{total_distance:.1f} km")
with col2:
    st.metric("Total Cost", f"₹{total_cost:.0f}")
with col3:
    st.metric("On-Time %", f"{on_time_percent}%")
with col4:
    st.metric("Vehicles Used", vehicles_used)

st.markdown("---")

# =========================
# BUILD MAP
# =========================

# Center map: either from first delivery or default Delhi
center_lat = 28.6
center_lng = 77.2
if deliveries:
    center_lat = deliveries[0].get("lat", center_lat)
    center_lng = deliveries[0].get("lng", center_lng)

m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

# ---- Draw roads with traffic color ----
def traffic_color(speed):
    if speed >= 30:
        return "green"
    elif speed >= 15:
        return "orange"
    else:
        return "red"

for road in roads:
    start = road.get("start")
    end = road.get("end")
    speed = road.get("speed_kmh", 30)
    if not start or not end:
        continue
    color = traffic_color(speed)
    folium.PolyLine(
        locations=[start, end],
        color=color,
        weight=4,
        opacity=0.8,
        tooltip=f"Speed: {speed} km/h",
    ).add_to(m)

# ---- Draw vehicle routes ----
for route in routes:
    path = route.get("path", [])
    if len(path) < 2:
        continue
    color = route.get("color", "blue")
    vid = route.get("vehicle_id", "V?")
    folium.PolyLine(
        locations=path,
        color=color,
        weight=5,
        opacity=0.9,
        tooltip=f"{vid} route",
    ).add_to(m)

    # Add a marker for the vehicle start
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color=color, icon="truck", prefix="fa"),
        tooltip=f"Vehicle {vid}",
    ).add_to(m)

# ---- Mark delivery locations ----
priority_icon_map = {
    "high": "exclamation-triangle",
    "medium": "info-sign",
    "low": "ok-sign",
}

for d in deliveries:
    lat = d.get("lat", d.get("location_lat"))
    lng = d.get("lng", d.get("location_lon"))

    raw_priority = d.get("priority", "low")

    if isinstance(raw_priority, int):
        priority = {
            1: "low",
            2: "low",
            3: "medium",
            4: "high",
            5: "high",
        }.get(raw_priority, "low")
    else:
        priority = str(raw_priority).lower()

    status = d.get("status", "unknown")
    d_id = d.get("id", "?")
    eta = d.get("eta", "-")

    if lat is None or lng is None:
        continue

    icon_name = priority_icon_map.get(priority, "ok-sign")
    color_map = {
        "high": "red",
        "medium": "orange",
        "low": "green",
    }
    marker_color = color_map.get(priority, "blue")

    tooltip_text = f"{d_id} | {priority} | {status} | ETA: {eta}"

    folium.Marker(
        location=[lat, lng],
        icon=folium.Icon(
            color=marker_color,
            icon=icon_name,
            prefix="fa"
        ),
        tooltip=tooltip_text,
    ).add_to(m)
   

# =========================
# SHOW MAP
# =========================

folium_static(m)

# =========================
# AUTO-REFRESH EVERY 5 SEC
# =========================

time.sleep(5)
st.rerun()