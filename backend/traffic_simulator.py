import networkx as nx
import random
from datetime import datetime
import time


class TrafficSimulator:

    # ==========================================
    # INITIALIZE TRAFFIC SIMULATOR
    # ==========================================

    def __init__(self):

        # Create a 10 x 10 grid road network
        # This gives 100 nodes
        self.graph = nx.grid_2d_graph(10, 10)

        # Dictionary to store traffic information
        self.traffic = {}

        # Initialize traffic data
        self.initialize_traffic()

    # ==========================================
    # CREATE TRAFFIC DATA FOR ALL ROADS
    # ==========================================

    def initialize_traffic(self):

        for edge in self.graph.edges():

            # Normal/free-flow speed of the road
            free_flow_speed = random.randint(40, 60)

            self.traffic[edge] = {
                "free_flow_speed": free_flow_speed,
                "current_speed": free_flow_speed,
                "congestion": 0.0
            }

    # ==========================================
    # GET CURRENT SPEED
    # ==========================================

    def get_current_speed(self, edge_id):

        if edge_id not in self.traffic:
            return None

        return self.traffic[edge_id]["current_speed"]

    # ==========================================
    # GET ROAD INFORMATION
    # ==========================================

    def get_road_info(self, edge_id):

        if edge_id not in self.traffic:
            return None

        data = self.traffic[edge_id]

        return {
            "edge_id": edge_id,
            "current_speed": data["current_speed"],
            "free_flow_speed": data["free_flow_speed"],
            "congestion": data["congestion"],
            "traffic_level": self.get_traffic_level(edge_id)
        }

    # ==========================================
    # TIME-BASED TRAFFIC MULTIPLIER
    # ==========================================

    def get_time_multiplier(self):

        hour = datetime.now().hour

        # Morning rush hour
        if 8 <= hour <= 10:
            return 0.5

        # Evening rush hour
        elif 17 <= hour <= 20:
            return 0.5

        # Night time
        elif 23 <= hour or hour <= 5:
            return 1.3

        # Normal time
        else:
            return 1.0

    # ==========================================
    # UPDATE TRAFFIC ON ALL ROADS
    # ==========================================

    def update_traffic(self):

        multiplier = self.get_time_multiplier()

        for edge_id, data in self.traffic.items():

            free_speed = data["free_flow_speed"]

            # Small random traffic variation
            random_factor = random.uniform(0.8, 1.1)

            # Calculate new speed
            new_speed = (
                free_speed
                * multiplier
                * random_factor
            )

            # Minimum speed = 5 km/h
            data["current_speed"] = max(
                5,
                round(new_speed, 2)
            )

            # Calculate congestion
            data["congestion"] = round(
                1 - (
                    data["current_speed"]
                    / free_speed
                ),
                2
            )

            # Keep congestion between 0 and 1
            data["congestion"] = max(
                0,
                min(
                    1,
                    data["congestion"]
                )
            )

    # ==========================================
    # SIMULATE TRAFFIC JAM / ACCIDENT
    # ==========================================

    def generate_congestion_event(self):

        # Select a random road
        edge_id = random.choice(
            list(self.traffic.keys())
        )

        # Reduce speed because of traffic jam
        self.traffic[edge_id]["current_speed"] = random.randint(
            5,
            15
        )

        # Mark road as highly congested
        self.traffic[edge_id]["congestion"] = 0.9

        # Return affected road
        return edge_id

    # ==========================================
    # GET TRAFFIC LEVEL
    # ==========================================

    def get_traffic_level(self, edge_id):

        if edge_id not in self.traffic:
            return "UNKNOWN"

        congestion = self.traffic[edge_id]["congestion"]

        if congestion < 0.3:
            return "LOW"

        elif congestion < 0.7:
            return "MEDIUM"

        else:
            return "HIGH"

    # ==========================================
    # GET ALL RAW TRAFFIC DATA
    # ==========================================

    def get_all_traffic(self):

        return self.traffic

    # ==========================================
    # GET FORMATTED TRAFFIC DATA
    # FOR OTHER TEAM MEMBERS / API / FRONTEND
    # ==========================================

    def get_traffic_data(self):

        traffic_data = []

        for edge_id, data in self.traffic.items():

            traffic_data.append({

                "edge_id": edge_id,

                "free_flow_speed":
                    data["free_flow_speed"],

                "current_speed":
                    data["current_speed"],

                "congestion":
                    data["congestion"],

                "traffic_level":
                    self.get_traffic_level(edge_id)
            })

        return traffic_data


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    traffic = TrafficSimulator()

    print("================================")
    print("TRAFFIC SIMULATOR")
    print("================================")

    # ------------------------------------------
    # Test road network
    # ------------------------------------------

    print(
        "Total nodes:",
        len(traffic.graph.nodes)
    )

    print(
        "Total roads:",
        len(traffic.graph.edges)
    )

    # ------------------------------------------
    # Initial traffic update
    # ------------------------------------------

    traffic.update_traffic()

    first_edge = list(
        traffic.traffic.keys()
    )[0]

    print(
        "\nRoad:",
        first_edge
    )

    print(
        "Speed:",
        traffic.get_current_speed(first_edge),
        "km/h"
    )

    print(
        "Traffic level:",
        traffic.get_traffic_level(first_edge)
    )

    # ------------------------------------------
    # Test road information
    # ------------------------------------------

    print(
        "\n--- Road Information Test ---"
    )

    print(
        traffic.get_road_info(first_edge)
    )

    # ------------------------------------------
    # Simulate traffic jam
    # ------------------------------------------

    print(
        "\n--- Simulating Traffic Jam ---"
    )

    affected_edge = (
        traffic.generate_congestion_event()
    )

    print(
        "Affected road:",
        affected_edge
    )

    print(
        "New speed:",
        traffic.get_current_speed(
            affected_edge
        ),
        "km/h"
    )

    print(
        "New traffic level:",
        traffic.get_traffic_level(
            affected_edge
        )
    )

    # ------------------------------------------
    # Test formatted traffic data
    # ------------------------------------------

    print(
        "\n--- Traffic Data Test ---"
    )

    traffic_data = (
        traffic.get_traffic_data()
    )

    print(
        "Total traffic records:",
        len(traffic_data)
    )

    print(
        "First traffic record:"
    )

    print(
        traffic_data[0]
    )

    # ------------------------------------------
    # Automatic traffic updates
    # ------------------------------------------

    print(
        "\n--- Automatic Traffic Update Test ---"
    )

    for i in range(3):

        print(
            f"\nTraffic update {i + 1}"
        )

        # Update all road traffic
        traffic.update_traffic()

        # Select first road for testing
        first_edge = list(
            traffic.traffic.keys()
        )[0]

        print(
            "Road:",
            first_edge
        )

        print(
            "Current speed:",
            traffic.get_current_speed(
                first_edge
            ),
            "km/h"
        )

        print(
            "Traffic level:",
            traffic.get_traffic_level(
                first_edge
            )
        )

        # Wait 30 seconds before next update
        if i < 2:

            print(
                "Next update in 30 seconds..."
            )

            time.sleep(30)

    # ------------------------------------------
    # Final message
    # ------------------------------------------

    print(
        "\n================================"
    )

    print(
        "TRAFFIC SIMULATOR TEST COMPLETE"
    )

    print(
        "================================"
    )