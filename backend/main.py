from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from shared_models import Order, Vehicle, Route
from database import db
from sample_data import create_sample_orders, create_sample_vehicles
from routing_engine import RoutingEngine
from cost_optimizer import CostOptimizer
from traffic_simulator import TrafficSimulator
from reoptimizer import Reoptimizer

# Create the FastAPI application
app = FastAPI(
    title="AI Last-Mile Logistics Platform",
    description="Real-time route optimization with traffic, capacity, and priority constraints",
    version="1.0.0"
)
routing_engine = RoutingEngine()
cost_optimizer = CostOptimizer()
traffic_simulator = TrafficSimulator()
reoptimizer = Reoptimizer(routing_engine, traffic_simulator)
# Enable CORS (allows frontend to call this API)
# This is like giving permission to other websites to talk to your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (fine for prototype)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# This function runs when server starts
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting AI Last-Mile Logistics Platform...")
    
    # Load sample data into database
    orders = create_sample_orders()
    vehicles = create_sample_vehicles()
    
    for order in orders:
        db.add_order(order)
    
    for vehicle in vehicles:
        db.add_vehicle(vehicle)
    
    print("✅ Sample data loaded successfully")
    print(f"📦 Total orders: {len(orders)}")
    print(f"🚚 Total vehicles: {len(vehicles)}")

# ============ BASIC ENDPOINTS ============

# Root endpoint - shows when you visit http://localhost:8000/
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Last-Mile Logistics Platform",
        "status": "running",
        "docs": "http://localhost:8000/docs"
    }

# Health check endpoint - used to verify API is working
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2026-08-17"}

# ============ ORDER ENDPOINTS ============

# Get all orders - GET http://localhost:8000/api/v1/orders
@app.get("/api/v1/orders", response_model=List[Order])
def get_all_orders():
    """
    Returns all delivery orders from database.
    Used by frontend to display orders table.
    """
    orders = db.get_all_orders()
    print(f"📦 Returning {len(orders)} orders")
    return orders

# Create a new order - POST http://localhost:8000/api/v1/orders
@app.post("/api/v1/orders")
def create_order(order: Order):
    """
    Adds a new delivery order to database.
    Frontend calls this when user clicks "Add Order" button.
    """
    db.add_order(order)
    print(f"✅ Created new order: {order.id}")
    return {
        "message": "Order created successfully",
        "order_id": order.id,
        "customer_name": order.customer_name
    }

# ============ VEHICLE ENDPOINTS ============

# Get all vehicles - GET http://localhost:8000/api/v1/vehicles
@app.get("/api/v1/vehicles", response_model=List[Vehicle])
def get_all_vehicles():
    """
    Returns all delivery vehicles from database.
    Used by frontend to show vehicle locations on map.
    """
    vehicles = db.get_all_vehicles()
    print(f"🚚 Returning {len(vehicles)} vehicles")
    return vehicles

# ============ ROUTE ENDPOINTS ============

# Get current routes - GET http://localhost:8000/api/v1/routes
@app.get("/api/v1/routes", response_model=List[Route])
def get_current_routes():
    """
    Returns optimized delivery routes.
    Initially empty, populated after calling /optimize endpoint.
    """
    routes = db.routes
    print(f"🗺️ Returning {len(routes)} routes")
    return routes

# Optimize routes - POST http://localhost:8000/api/v1/optimize
@app.post("/api/v1/optimize")
def optimize_routes():
    """Generate optimized delivery routes."""
    try:
        print("🚀 Optimization started...")

        orders = db.get_pending_orders()
        vehicles = db.get_all_vehicles()

        print(f"📦 Orders to optimize: {len(orders)}")
        print(f"🚚 Available vehicles: {len(vehicles)}")

        routes = routing_engine.solve_routes(orders, vehicles)

        db.update_routes(routes)

        total_distance = sum(
            route.total_distance_km for route in routes
        )

        total_cost = sum(
            route.estimated_cost for route in routes
        )

        return {
            "message": "Route optimization completed successfully",
            "orders_count": len(orders),
            "vehicles_count": len(vehicles),
            "routes": routes,
            "total_distance_km": total_distance,
            "total_cost": total_cost
        }

    except Exception as error:
        print(f"❌ Optimization error: {error}")

        return {
            "message": "Optimization failed",
            "error": str(error)
        }

# Re-optimize routes - POST http://localhost:8000/api/v1/reoptimize
@app.post("/api/v1/reoptimize")
def reoptimize_routes():
    """
    Trigger dynamic re-optimization based on traffic changes.
    Calls Person 4's reoptimizer module.
    """
    print("🔄 Re-optimization triggered...")

    orders = db.get_pending_orders()
    vehicles = db.get_all_vehicles()
    current_routes = db.routes

    new_routes = reoptimizer.reoptimize_routes(
        orders=orders,
        vehicles=vehicles,
        current_routes=current_routes
    )

    db.update_routes(new_routes)

    # Compute updated analytics
    analytics = cost_optimizer.calculate_total_cost(
        routes=new_routes,
        orders=orders,
        vehicles=vehicles
    )

    kpis = cost_optimizer.calculate_kpis(
        routes=new_routes,
        orders=orders,
        vehicles=vehicles
    )

    baseline = cost_optimizer.calculate_baseline(
        orders=orders,
        vehicles=vehicles
    )

    savings = cost_optimizer.calculate_savings(
        optimized_cost=analytics["total_cost"],
        baseline_cost=baseline["total_cost"]
    )

    return {
        "message": "Re-optimization completed successfully",
        "orders_count": len(orders),
        "vehicles_count": len(vehicles),
        "routes": new_routes,
        "total_distance_km": analytics["total_distance_km"],
        "total_cost": analytics["total_cost"],
        "kpis": kpis,
        "baseline": baseline,
        "savings": savings
    }

# ============ ANALYTICS ENDPOINT ============

# Get analytics - GET http://localhost:8000/api/v1/analytics
@app.get("/api/v1/analytics")
def get_analytics():
    """
    Returns cost and performance analytics.
    Calls Person 6's cost optimizer module.
    """
    print("📊 Analytics requested...")

    orders = db.get_all_orders()
    vehicles = db.get_all_vehicles()

    # Use routing engine
    routes = routing_engine.solve_routes(orders, vehicles)

    # Use cost optimizer
    analytics = cost_optimizer.calculate_total_cost(
        routes=routes,
        orders=orders,
        vehicles=vehicles
    )

    kpis = cost_optimizer.calculate_kpis(
        routes=routes,
        orders=orders,
        vehicles=vehicles
    )

    baseline = cost_optimizer.calculate_baseline(
        orders=orders,
        vehicles=vehicles
    )

    savings = cost_optimizer.calculate_savings(
        optimized_cost=analytics["total_cost"],
        baseline_cost=baseline["total_cost"]
    )

    return {
        "message": "Analytics generated successfully",
        "total_cost": analytics["total_cost"],
        "total_distance_km": analytics["total_distance_km"],
        "avg_cost_per_order": analytics["avg_cost_per_order"],
        "cost_breakdown": analytics["cost_breakdown"],
        "routes": analytics["routes"],
        "kpis": kpis,
        "baseline": baseline,
        "savings": savings
    }

# ============ DEMO ENDPOINT ============

# Traffic jam demo - POST http://localhost:8000/api/v1/demo/traffic-jam
@app.post("/api/v1/demo/traffic-jam")
def demo_traffic_jam():
    """
    For demo purposes: simulates traffic jam and re-optimizes.
    Calls Person 3's traffic simulator + re-optimizes routes.
    """
    print("🚗 Traffic jam simulation triggered...")

    # 1. Update traffic (optional, to refresh speeds)
    traffic_simulator.update_traffic()

    # 2. Generate a congestion event (traffic jam on one edge)
    affected_edge = traffic_simulator.generate_congestion_event()
    print(f"🚧 Traffic jam on edge: {affected_edge}")

    # 3. Re-run optimization with current data
    orders = db.get_pending_orders()
    vehicles = db.get_all_vehicles()

    print(f"📦 Orders to optimize: {len(orders)}")
    print(f"🚚 Available vehicles: {len(vehicles)}")

    routes = routing_engine.solve_routes(orders, vehicles)

    db.update_routes(routes)

    # 4. Compute analytics with cost optimizer
    analytics = cost_optimizer.calculate_total_cost(
        routes=routes,
        orders=orders,
        vehicles=vehicles
    )

    kpis = cost_optimizer.calculate_kpis(
        routes=routes,
        orders=orders,
        vehicles=vehicles
    )

    baseline = cost_optimizer.calculate_baseline(
        orders=orders,
        vehicles=vehicles
    )

    savings = cost_optimizer.calculate_savings(
        optimized_cost=analytics["total_cost"],
        baseline_cost=baseline["total_cost"]
    )

    # 5. Return response
    return {
        "message": "Traffic jam simulated and routes re-optimized",
        "affected_edge": affected_edge,
        "traffic_level": traffic_simulator.get_traffic_level(affected_edge),
        "orders_count": len(orders),
        "vehicles_count": len(vehicles),
        "routes": routes,
        "total_distance_km": analytics["total_distance_km"],
        "total_cost": analytics["total_cost"],
        "kpis": kpis,
        "baseline": baseline,
        "savings": savings
    }
# ============ RUN THE SERVER ============

# This code runs when you execute: python main.py
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting AI Last-Mile Logistics API Server")
    print("="*60)
    print("📍 Open browser: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("💚 Health check: http://localhost:8000/health")
    print("="*60 + "\n")
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)