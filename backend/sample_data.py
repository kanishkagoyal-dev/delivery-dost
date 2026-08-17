from backend.shared_models import Order, Vehicle, PriorityLevel
from datetime import datetime, timedelta

# This function creates 20 sample delivery orders
def create_sample_orders():
    orders = []
    base_time = datetime.now()  # Current time
    
    # Create 20 orders with different locations and priorities
    for i in range(20):
        order = Order(
            id=f"ORD-{i+1:03d}",  # ORD-001, ORD-002, etc.
            customer_name=f"Customer {i+1}",  # Customer 1, Customer 2, etc.
            location_lat=28.6 + (i * 0.01),  # Slightly different latitude
            location_lon=77.2 + (i * 0.01),  # Slightly different longitude
            priority=PriorityLevel((i % 5) + 1),  # Cycles through priorities 1-5
            time_window_start=base_time + timedelta(hours=i),  # Delivery window starts i hours from now
            time_window_end=base_time + timedelta(hours=i+3),  # Ends 3 hours later
            package_weight_kg=2.5 + (i * 0.5),  # Weight increases with order number
            package_volume_m3=0.01 + (i * 0.002)  # Volume increases slightly
        )
        orders.append(order)
    
    print(f"✅ Created {len(orders)} sample orders")
    return orders

# This function creates 5 sample delivery vehicles
def create_sample_vehicles():
    vehicles = []
    
    # Create 5 vehicles with different costs
    for i in range(5):
        vehicle = Vehicle(
            id=f"VEH-{i+1:02d}",  # VEH-01, VEH-02, etc.
            driver_name=f"Driver {i+1}",  # Driver 1, Driver 2, etc.
            current_lat=28.6139,  # All start at same location (Delhi)
            current_lon=77.2090,
            capacity_weight_kg=100,  # Can carry 100 kg
            capacity_volume_m3=0.5,  # Can carry 0.5 cubic meters
            cost_per_km=15 + (i * 2)  # Cost increases: 15, 17, 19, 21, 23 ₹/km
        )
        vehicles.append(vehicle)
    
    print(f"✅ Created {len(vehicles)} sample vehicles")
    return vehicles
