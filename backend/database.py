from typing import List, Dict
from shared_models import Order, Vehicle, Route

# This is a simple in-memory database (stores data in RAM)
# For prototype, we don't need a real database
class InMemoryDB:
    def __init__(self):
        # Initialize empty dictionaries to store data
        self.orders: Dict[str, Order] = {}      # Orders stored by ID
        self.vehicles: Dict[str, Vehicle] = {}  # Vehicles stored by ID
        self.routes: List[Route] = []           # List of routes
    
    # Add a new order to database
    def add_order(self, order: Order):
        self.orders[order.id] = order
        print(f"✅ Added order: {order.id}")
    
    # Add a new vehicle to database
    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles[vehicle.id] = vehicle
        print(f"✅ Added vehicle: {vehicle.id}")
    
    # Get all orders
    def get_all_orders(self) -> List[Order]:
        return list(self.orders.values())
    
    # Get all vehicles
    def get_all_vehicles(self) -> List[Vehicle]:
        return list(self.vehicles.values())
    
    # Get only pending orders (not yet assigned to routes)
    def get_pending_orders(self) -> List[Order]:
        return [o for o in self.orders.values() if o.status == "pending"]
    
    # Update routes
    def update_routes(self, routes: List[Route]):
        self.routes = routes
        print(f"✅ Updated {len(routes)} routes")

# Create a global database instance that all files can use
db = InMemoryDB()