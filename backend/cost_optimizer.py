from typing import List, Dict, Any
from backend.shared_models import Order, Vehicle, Route, PriorityLevel


class CostOptimizer:
    def __init__(
        self,
        fuel_rate_per_km: float = 12.0,
        driver_wage_per_hour: float = 150.0,
        vehicle_fixed_cost: float = 100.0,
        late_penalty_per_minute: float = 5.0,
    ):
        self.fuel_rate_per_km = fuel_rate_per_km
        self.driver_wage_per_hour = driver_wage_per_hour
        self.vehicle_fixed_cost = vehicle_fixed_cost
        self.late_penalty_per_minute = late_penalty_per_minute

    def fuel_cost(self, route: Route) -> float:
        return route.total_distance_km * self.fuel_rate_per_km

    def driver_cost(self, route: Route) -> float:
        return (route.total_time_minutes / 60.0) * self.driver_wage_per_hour

    def late_penalty(self, route: Route, orders: List[Order]) -> float:
        order_map = {o.id: o for o in orders}
        total = 0.0

        for order_id in route.order_ids:
            order = order_map.get(order_id)
            if not order:
                continue

            # Use time_window_end as deadline
            deadline = order.time_window_end
            actual = route.end_time

            if actual > deadline:
                late_minutes = (actual - deadline).total_seconds() / 60.0
                total += late_minutes * self.late_penalty_per_minute

        return total

    def route_cost(
        self, route: Route, orders: List[Order]
    ) -> Dict[str, float]:
        fuel = self.fuel_cost(route)
        driver = self.driver_cost(route)
        vehicle_fixed = self.vehicle_fixed_cost
        penalty = self.late_penalty(route, orders)

        return {
            "fuel": fuel,
            "driver": driver,
            "vehicle": vehicle_fixed,
            "late_penalties": penalty,
            "total": fuel + driver + vehicle_fixed + penalty,
        }

    def calculate_total_cost(
        self,
        routes: List[Route],
        orders: List[Order],
        vehicles: List[Vehicle],
    ) -> Dict[str, Any]:
        vehicle_map = {v.id: v for v in vehicles}
        order_map = {o.id: o for o in orders}

        breakdown = {
            "fuel": 0.0,
            "driver": 0.0,
            "vehicle": 0.0,
            "late_penalties": 0.0,
        }

        route_results = []
        total_distance = 0.0

        for route in routes:
            route_orders = [order_map[x] for x in route.order_ids]
            result = self.route_cost(route, route_orders)
            total_distance += route.total_distance_km

            for key in breakdown:
                breakdown[key] += result[key]

            route_results.append(
                {
                    "vehicle_id": route.vehicle_id,
                    "orders": route.order_ids,
                    "distance_km": route.total_distance_km,
                    "travel_time_min": route.total_time_minutes,
                    **result,
                }
            )

        total_cost = sum(breakdown.values())
        order_count = len(orders)

        return {
            "total_cost": round(total_cost, 2),
            "total_distance_km": round(total_distance, 2),
            "avg_cost_per_order": round(
                total_cost / order_count, 2
            ) if order_count else 0,
            "cost_breakdown": {
                k: round(v, 2) for k, v in breakdown.items()
            },
            "routes": route_results,
        }

    def calculate_kpis(
        self,
        routes: List[Route],
        orders: List[Order],
        vehicles: List[Vehicle],
    ) -> Dict[str, Any]:
        order_map = {o.id: o for o in orders}

        on_time = 0
        total_orders_in_routes = 0

        for route in routes:
            for order_id in route.order_ids:
                order = order_map.get(order_id)
                if not order:
                    continue

                total_orders_in_routes += 1
                if route.end_time <= order.time_window_end:
                    on_time += 1

        used_vehicle_ids = {r.vehicle_id for r in routes}

        return {
            "total_orders": len(orders),
            "vehicles_available": len(vehicles),
            "vehicles_used": len(used_vehicle_ids),
            "vehicle_utilization_percent": round(
                len(used_vehicle_ids) / len(vehicles) * 100, 2
            ) if vehicles else 0,
            "on_time_delivery_percent": round(
                on_time / total_orders_in_routes * 100, 2
            ) if total_orders_in_routes else 0,
        }

    def calculate_baseline(
        self,
        orders: List[Order],
        vehicles: List[Vehicle],
        km_per_order: float = 5.0,
        minutes_per_order: float = 20.0,
    ) -> Dict[str, float]:
        if not orders or not vehicles:
            return {"total_cost": 0.0, "distance_km": 0.0}

        total_distance = len(orders) * km_per_order
        total_time = len(orders) * minutes_per_order

        avg_fuel = self.fuel_rate_per_km
        avg_wage = self.driver_wage_per_hour
        fixed_cost = self.vehicle_fixed_cost

        fuel = total_distance * avg_fuel
        driver = (total_time / 60.0) * avg_wage

        baseline_cost = fuel + driver + fixed_cost

        return {
            "total_cost": round(baseline_cost, 2),
            "distance_km": round(total_distance, 2),
        }

    def calculate_savings(
        self, optimized_cost: float, baseline_cost: float
    ) -> Dict[str, float]:
        savings = baseline_cost - optimized_cost
        percentage = (
            savings / baseline_cost * 100 if baseline_cost else 0
        )

        return {
            "absolute_savings": round(savings, 2),
            "percentage_savings": round(percentage, 2),
        }

    def what_if_fuel_increase(
        self, analytics: Dict[str, Any], increase_percent: float
    ) -> Dict[str, float]:
        old_fuel = analytics["cost_breakdown"]["fuel"]
        new_fuel = old_fuel * (1 + increase_percent / 100.0)

        new_total = analytics["total_cost"] - old_fuel + new_fuel

        return {
            "old_total_cost": round(analytics["total_cost"], 2),
            "new_total_cost": round(new_total, 2),
            "change": round(new_total - analytics["total_cost"], 2),
        }

    def what_if_vehicle_scenario(
        self,
        current_analytics: Dict[str, Any],
        current_vehicle_count: int,
        new_vehicle_count: int,
        simulated_new_cost: float,
    ) -> Dict[str, float]:
        return {
            "old_vehicle_count": current_vehicle_count,
            "new_vehicle_count": new_vehicle_count,
            "old_cost": round(current_analytics["total_cost"], 2),
            "new_cost": round(simulated_new_cost, 2),
            "change": round(
                simulated_new_cost - current_analytics["total_cost"], 2
            ),
        }
