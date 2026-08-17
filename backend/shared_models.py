from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

# This defines priority levels (1-5)
class PriorityLevel(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

# This is the blueprint for a Delivery Order
class Order(BaseModel):
    id: str                          # Unique order ID like "ORD-001"
    customer_name: str               # Customer's name
    location_lat: float              # Latitude (GPS coordinate)
    location_lon: float              # Longitude (GPS coordinate)
    priority: PriorityLevel          # 1-5 priority level
    time_window_start: datetime      # Earliest delivery time
    time_window_end: datetime        # Latest delivery time
    package_weight_kg: float         # Weight in kilograms
    package_volume_m3: float         # Volume in cubic meters
    status: str = "pending"          # Status: pending, assigned, delivered

# This is the blueprint for a Delivery Vehicle
class Vehicle(BaseModel):
    id: str                          # Vehicle ID like "VEH-01"
    driver_name: str                 # Driver's name
    current_lat: float               # Current GPS latitude
    current_lon: float               # Current GPS longitude
    capacity_weight_kg: float        # Max weight capacity
    capacity_volume_m3: float        # Max volume capacity
    cost_per_km: float               # Cost per kilometer
    speed_kmph: float = 40           # Average speed (default 40 km/h)
    status: str = "available"        # Status: available, busy, maintenance

# This is the blueprint for a Route (set of orders for one vehicle)
class Route(BaseModel):
    vehicle_id: str                  # Which vehicle
    order_ids: List[str]             # List of order IDs to deliver
    total_distance_km: float         # Total distance in km
    total_time_minutes: float        # Total time in minutes
    estimated_cost: float            # Estimated cost in rupees
    start_time: datetime             # When route starts
    end_time: datetime               # When route ends
