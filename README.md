# DeliveryDost

**The brain behind every better delivery.**

AI-powered last-mile routing for delivery fleets. Built for Internal SIH 2026.

---

## Team Members

- **Kanishka Goyal**: Backend & API  
- **Mahima Agarwal**: Routing Engine  
- **Himanshi Garg**: Traffic Simulator  
- **Mayra Sinsinwar**: Re-optimization  
- **Anvi Jain**: Frontend Dashboard  
- **Gauri**: Cost Optimization  

---

## Problem Statement

Develop an AI-powered last-mile logistics optimization platform that dynamically determines delivery routes by considering real-time traffic, vehicle capacity, delivery priorities, time constraints, and operational costs.

---

## Solution Overview

DeliveryDost is an AI-powered last-mile logistics platform that:

- Dynamically generates optimized delivery routes  
- Considers real-time traffic conditions and simulated traffic jams  
- Respects vehicle capacity (weight & volume)  
- Handles delivery priorities and time windows  
- Minimizes operational costs (fuel, distance, time)  

---

## Setup Instructions

1. Install Python 3.11+
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate        # Windows
   source venv/bin/activate       # Mac / Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run backend server:
   ```bash
   cd backend
   python main.py
   ```
5. Open API docs in browser:
   ```text
   http://localhost:8000/docs
   ```

---

## API Endpoints

- `GET  /api/v1/orders` – Get all orders  
- `POST /api/v1/orders` – Add new order  
- `GET  /api/v1/vehicles` – Get all vehicles  
- `GET  /api/v1/routes` – Get optimized routes  
- `POST /api/v1/optimize` – Trigger optimization  
- `POST /api/v1/reoptimize` – Trigger re-optimization  
- `GET  /api/v1/analytics` – Get cost analytics  
- `POST /api/v1/demo/traffic-jam` – Demo traffic jam  

---

## Tech Stack

- **Backend**: FastAPI, Pydantic  
- **Routing**: Google OR-Tools  
- **Frontend**: Streamlit, Folium  
- **Maps**: OpenStreetMap  

---

## How to Use (Quick Demo Flow)

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```
2. Open API docs:
   ```text
   http://localhost:8000/docs
   ```
3. Add sample orders and vehicles via `/api/v1/orders` and `/api/v1/vehicles`.
4. Call `/api/v1/optimize` to generate optimized routes.
5. View routes and analytics via `/api/v1/routes` and `/api/v1/analytics`.
6. Use `/api/v1/demo/traffic-jam` to simulate a traffic jam and then call `/api/v1/reoptimize`.

---

*Built for Internal SIH 2026 – Problem Statement ID: S14*