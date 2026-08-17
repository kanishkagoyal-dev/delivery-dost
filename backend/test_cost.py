from backend.routing_engine import RoutingEngine
from backend.cost_optimizer import CostOptimizer
from backend.sample_data import create_sample_orders, create_sample_vehicles

orders = create_sample_orders()
vehicles = create_sample_vehicles()

routing_engine = RoutingEngine()
routes = routing_engine.solve_routes(orders, vehicles)

cost_optimizer = CostOptimizer()

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

print("\n=== COST ANALYTICS ===")
print(analytics)

print("\n=== KPIs ===")
print(kpis)

print("\n=== BASELINE ===")
print(baseline)

print("\n=== SAVINGS ===")
print(savings)
