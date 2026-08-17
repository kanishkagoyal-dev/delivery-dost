from datetime import datetime, timedelta
from typing import List
import math

from backend.shared_models import Order, Route, Vehicle


class RoutingEngine:
    """Greedy route optimizer for pending delivery orders."""

    DEFAULT_START_TIME = datetime(2026, 8, 16, 10, 0, 0)
    SERVICE_TIME_MINUTES = 5.0

    def solve_routes(
        self,
        orders: List[Order],
        vehicles: List[Vehicle],
    ) -> List[Route]:
        """Assign valid pending orders to available vehicles."""
        if not orders or not vehicles:
            return []

        pending_orders = [
            order for order in orders
            if order.status == "pending"
        ]

        available_vehicles = [
            vehicle for vehicle in vehicles
            if vehicle.status == "available"
        ]

        pending_orders.sort(
            key=lambda order: order.priority.value,
            reverse=True,
        )

        available_vehicles.sort(
            key=lambda vehicle: vehicle.capacity_weight_kg,
            reverse=True,
        )

        routes: List[Route] = []
        assigned_order_ids = set()

        for vehicle in available_vehicles:
            selected_orders: List[Order] = []
            total_weight = 0.0
            total_volume = 0.0

            for order in pending_orders:
                if order.id in assigned_order_ids:
                    continue

                new_weight = total_weight + order.package_weight_kg
                new_volume = total_volume + order.package_volume_m3

                if new_weight > vehicle.capacity_weight_kg:
                    continue

                if new_volume > vehicle.capacity_volume_m3:
                    continue

                candidate_orders = selected_orders + [order]

                if not self._route_is_time_feasible(
                    vehicle,
                    candidate_orders,
                ):
                    continue

                selected_orders.append(order)
                assigned_order_ids.add(order.id)
                total_weight = new_weight
                total_volume = new_volume

            if selected_orders:
                routes.append(
                    self._build_route(vehicle, selected_orders)
                )

        return routes

    def _build_route(
        self,
        vehicle: Vehicle,
        orders: List[Order],
    ) -> Route:
        ordered_orders = self._nearest_neighbor_ordering(
            vehicle,
            orders,
        )

        total_distance_km = self._calculate_route_distance(
            vehicle,
            ordered_orders,
        )

        speed_kmph = max(vehicle.speed_kmph, 1.0)
        travel_time_minutes = (
            total_distance_km / speed_kmph
        ) * 60.0
        service_time_minutes = (
            len(ordered_orders) * self.SERVICE_TIME_MINUTES
        )
        total_time_minutes = (
            travel_time_minutes + service_time_minutes
        )
        estimated_cost = total_distance_km * vehicle.cost_per_km

        start_time = self.DEFAULT_START_TIME
        end_time = start_time + timedelta(
            minutes=total_time_minutes
        )

        return Route(
            vehicle_id=vehicle.id,
            order_ids=[order.id for order in ordered_orders],
            total_distance_km=round(total_distance_km, 2),
            total_time_minutes=round(total_time_minutes, 2),
            estimated_cost=round(estimated_cost, 2),
            start_time=start_time,
            end_time=end_time,
        )

    def _nearest_neighbor_ordering(
        self,
        vehicle: Vehicle,
        orders: List[Order],
    ) -> List[Order]:
        remaining_orders = list(orders)
        ordered_orders: List[Order] = []
        current_lat = vehicle.current_lat
        current_lon = vehicle.current_lon

        while remaining_orders:
            nearest_order = min(
                remaining_orders,
                key=lambda order: self._calculate_distance(
                    current_lat,
                    current_lon,
                    order.location_lat,
                    order.location_lon,
                ),
            )
            ordered_orders.append(nearest_order)
            remaining_orders.remove(nearest_order)
            current_lat = nearest_order.location_lat
            current_lon = nearest_order.location_lon

        return ordered_orders

    def _route_is_time_feasible(
        self,
        vehicle: Vehicle,
        orders: List[Order],
    ) -> bool:
        ordered_orders = self._nearest_neighbor_ordering(
            vehicle,
            orders,
        )
        current_time = self.DEFAULT_START_TIME
        current_lat = vehicle.current_lat
        current_lon = vehicle.current_lon
        speed_kmph = max(vehicle.speed_kmph, 1.0)

        for order in ordered_orders:
            distance_km = self._calculate_distance(
                current_lat,
                current_lon,
                order.location_lat,
                order.location_lon,
            )
            travel_minutes = (
                distance_km / speed_kmph
            ) * 60.0
            current_time += timedelta(minutes=travel_minutes)

            if current_time < order.time_window_start:
                current_time = order.time_window_start

            if current_time > order.time_window_end:
                return False

            current_time += timedelta(
                minutes=self.SERVICE_TIME_MINUTES
            )
            current_lat = order.location_lat
            current_lon = order.location_lon

        return True

    def _calculate_route_distance(
        self,
        vehicle: Vehicle,
        orders: List[Order],
    ) -> float:
        total_distance = 0.0
        current_lat = vehicle.current_lat
        current_lon = vehicle.current_lon

        for order in orders:
            total_distance += self._calculate_distance(
                current_lat,
                current_lon,
                order.location_lat,
                order.location_lon,
            )
            current_lat = order.location_lat
            current_lon = order.location_lon

        return total_distance

    def _calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """Return great-circle distance in kilometres."""
        earth_radius_km = 6371.0
        lat1_radians = math.radians(lat1)
        lat2_radians = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        value = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_radians)
            * math.cos(lat2_radians)
            * math.sin(delta_lon / 2) ** 2
        )
        value = min(1.0, max(0.0, value))
        angle = 2 * math.atan2(
            math.sqrt(value),
            math.sqrt(1 - value),
        )
        return earth_radius_km * angle
