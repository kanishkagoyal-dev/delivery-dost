from typing import List
from shared_models import Order, Vehicle, Route


class Reoptimizer:
    def __init__(self, routing_engine, traffic_simulator):
        self.routing_engine = routing_engine
        self.traffic_simulator = traffic_simulator

    def reoptimize_routes(
        self,
        orders: List[Order],
        vehicles: List[Vehicle],
        current_routes: List[Route]
    ) -> List[Route]:
        """
        Refresh traffic conditions, then calculate fresh routes.

        Person 2's current routing engine does not yet accept
        traffic_data as an input, so traffic is updated here for
        the traffic module and dashboard.
        """
        self.traffic_simulator.update_traffic()
        traffic_data = self.traffic_simulator.get_traffic_data()

        new_routes = self.routing_engine.solve_routes(
            orders=orders,
            vehicles=vehicles
        )

        return new_routes