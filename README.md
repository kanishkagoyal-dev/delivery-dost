# AI Last-Mile Logistics Platform

## Team Members
- Person 1: Backend & API (You)
- Person 2: Routing Engine
- Person 3: Traffic Simulator
- Person 4: Re-optimization
- Person 5: Frontend Dashboard
- Person 6: Cost Optimization

## Setup Instructions

1. Install Python 3.11+
2. Create virtual environment: `python -m venv venv`
3. Activate: `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Run server: `cd backend && python main.py`
6. Open browser: http://localhost:8000/docs

## API Endpoints

- GET /api/v1/orders - Get all orders
- POST /api/v1/orders - Add new order
- GET /api/v1/vehicles - Get all vehicles
- GET /api/v1/routes - Get optimized routes
- POST /api/v1/optimize - Trigger optimization
- POST /api/v1/reoptimize - Trigger re-optimization
- GET /api/v1/analytics - Get cost analytics
- POST /api/v1/demo/traffic-jam - Demo traffic jam

## Tech Stack
- Backend: FastAPI, Pydantic
- Routing: Google OR-Tools
- Frontend: Streamlit, Folium
- Maps: OpenStreetMap