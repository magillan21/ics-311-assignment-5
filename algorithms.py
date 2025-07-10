import heapq
from typing import List, Tuple
from islands_graph import PolynesianGraph, create_polynesian_graph

# -------------------------------
# PERSON 1 - 
# ICS 311 Assignment: Polynesian Triangle
# This class implements 
# -------------------------------

class KnowledgeShareLeader:
    """Handles the knowledge sharing leader algorithm"""
    
    def __init__(self, graph: PolynesianGraph, starting_island: str):
        self.graph = graph
        self.starting_island = starting_island
        self.current_location = starting_island
        self.current_time = 0
        
    def calculate_island_priority(self, island_name: str) -> float:
        """
        Calculate priority score for visiting an island
        Higher score = higher priority
        
        Factors:
        - Population size (higher = more priority)
        - Recency (longer since last visit = more priority)
        - Never visited gets highest priority
        """
        island = self.graph.islands[island_name]
        
        # Base priority from population (normalize to 0-1 scale)
        max_pop = max(i.population for i in self.graph.islands.values())
        population_score = island.population / max_pop
        
        # Recency score
        if island.last_visited is None:
            recency_score = 2.0  # Never visited gets high priority
        else:
            time_since_visit = self.current_time - island.last_visited
            recency_score = min(time_since_visit / 10.0, 1.0)  # Normalize
        
        # Combined score (you can adjust weights)
        priority = (0.6 * population_score) + (0.4 * recency_score)
        return priority
    
    def find_shortest_path(self, start: str, end: str) -> Tuple[List[str], int]:
        """
        Find shortest path between two islands using Dijkstra's algorithm
        Returns (path, total_time)
        """
    # WIP
    #
    #
    
    def plan_knowledge_sharing_trip(self, max_trip_time: int) -> List[str]:
        """
        Plan a single knowledge sharing trip within time budget
        Returns list of islands to visit in order
        """
    # WIP
    #
    #
    
    def execute_trip(self, trip_plan: List[str]):
        """Execute a planned trip and update visit records"""
    # WIP
    #
    #
# -------------------------------
# PERSON 2 - Eric Chae
# ICS 311 Assignment: Polynesian Triangle
# This class implements a resource distribution algorithm that uses Dijkstra’s algorithm
# to efficiently deliver a resource produced in one island (e.g., Hawaii) to all others.
# Each canoe can carry only one unit per trip, and the goal is to minimize the total number of trips
# and use the shortest paths for delivery. The graph is represented as a directed, weighted network.
# -------------------------------

class ResourceDistributor:
    """
    Handles efficient distribution of a resource produced in only one island.
    Each canoe can only carry one unit, and we assume limited canoes per trip.
    """

    def __init__(self, graph: PolynesianGraph, resource_name: str, origin_island: str, total_units: int):
        self.graph = graph
        self.resource_name = resource_name  # e.g., "shells"
        self.origin_island = origin_island  # e.g., "Hawaii"
        self.total_units = total_units      # total supply available for distribution

    def dijkstra_all_paths(self, start: str) -> Dict[str, Tuple[int, List[str]]]:
        """
        Use Dijkstra’s algorithm to compute shortest travel times from the origin island
        to all other reachable islands.
        Returns a dictionary mapping each island to (travel_time, path).
        """
        heap = [(0, start, [])]  # (cumulative time, current island, path taken)
        distances = {}  # Final shortest times and paths

        while heap:
            time, node, path = heapq.heappop(heap)
            if node in distances:
                continue  # Already finalized
            distances[node] = (time, path + [node])  # Store shortest path to this node
            for neighbor, t in self.graph.get_neighbors(node):
                if neighbor not in distances:
                    heapq.heappush(heap, (time + t, neighbor, path + [node]))

        return distances

    def distribute_resources(self, canoe_capacity: int = 1) -> List[Tuple[str, int, List[str]]]:
        """
        Plan the distribution of the resource to each island from the origin island.
        Assumes 1 unit of the resource should go to each island.
        Returns a list of tuples: (destination_island, trips_needed, route).
        """
        distances = self.dijkstra_all_paths(self.origin_island)
        results = []

        for island_name, (time, path) in distances.items():
            if island_name == self.origin_island:
                continue  # Skip the origin island itself

            demand = 1  # Each island needs 1 unit of the resource
            trips_needed = -(-demand // canoe_capacity)  # Ceiling division

            # Append result as (island name, number of trips, route taken)
            results.append((island_name, trips_needed, path))

        # Sort islands by how many trips are needed (all are 1 here, but useful if scaled)
        return sorted(results, key=lambda x: x[1])
