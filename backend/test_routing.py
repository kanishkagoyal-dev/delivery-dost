from routing_engine import RoutingEngine
from sample_data import (
    create_sample_orders,
    create_sample_vehicles,
)


def test_routes_are_created():
    orders = create_sample_orders()
    vehicles = create_sample_vehicles()

    engine = RoutingEngine()
    routes = engine.solve_routes(
        orders,
        vehicles,
    )

    assert isinstance(routes, list)

    for route in routes:
        assert route.vehicle_id
        assert isinstance(route.order_ids, list)
        assert route.total_distance_km >= 0
        assert route.total_time_minutes >= 0
        assert route.estimated_cost >= 0


def test_orders_are_not_duplicated():
    orders = create_sample_orders()
    vehicles = create_sample_vehicles()

    engine = RoutingEngine()
    routes = engine.solve_routes(
        orders,
        vehicles,
    )

    assigned_order_ids = []

    for route in routes:
        assigned_order_ids.extend(route.order_ids)

    assert len(assigned_order_ids) == len(
        set(assigned_order_ids)
    )


def test_only_pending_orders_are_used():
    orders = create_sample_orders()
    vehicles = create_sample_vehicles()

    orders[0].status = "delivered"

    engine = RoutingEngine()
    routes = engine.solve_routes(
        orders,
        vehicles,
    )

    assigned_order_ids = []

    for route in routes:
        assigned_order_ids.extend(route.order_ids)

    assert orders[0].id not in assigned_order_ids


def test_zero_distance():
    engine = RoutingEngine()

    distance = engine._calculate_distance(
        26.8467,
        80.9462,
        26.8467,
        80.9462,
    )

    assert distance == 0.0


if __name__ == "__main__":
    orders = create_sample_orders()
    vehicles = create_sample_vehicles()

    engine = RoutingEngine()
    routes = engine.solve_routes(
        orders,
        vehicles,
    )

    print(f"Generated routes: {len(routes)}")

    for route in routes:
        print(route.model_dump())