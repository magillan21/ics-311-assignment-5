import heapq
from typing import List, Tuple, Dict
from polynesian_triangle import PolynesianGraph, create_polynesian_graph

# -------------------------------
# PERSON 1 - Michaela Gillan
# ICS 311 Assignment: Polynesian Triangle
# This class implements a knowledge sharing algorithm that utilizess Dijkstra's algorithm.
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
        if start == end:
            return ([start], 0)
        
        distances = {island: float('inf') for island in self.graph.islands}
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == end:
                # Reconstruct path
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                path.reverse()
                return (path, distances[end])
            
            for neighbor, travel_time in self.graph.get_neighbors(current):
                distance = current_dist + travel_time
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        return ([], float('inf'))  # No path found

    def plan_knowledge_sharing_trip(self, max_trip_time: int) -> List[str]:
        """
        Plan a single knowledge sharing trip within time budget
        Returns list of islands to visit in order
        """
        trip_plan = [self.starting_island]
        current_location = self.starting_island
        remaining_time = max_trip_time
        visited_this_trip = {self.starting_island}
        
        while True:
            # Find best unvisited island within time constraints
            best_island = None
            best_priority = -1
            best_path = []
            best_time = float('inf')
            
            for island_name in self.graph.get_island_names():
                if island_name in visited_this_trip:
                    continue
                    
                # Check if we can reach this island and return
                path_to_island, time_to_island = self.find_shortest_path(current_location, island_name)
                path_to_start, time_to_start = self.find_shortest_path(island_name, self.starting_island)
                
                total_time_needed = time_to_island + time_to_start
                
                if total_time_needed <= remaining_time:
                    priority = self.calculate_island_priority(island_name)
                    if priority > best_priority:
                        best_priority = priority
                        best_island = island_name
                        best_path = path_to_island
                        best_time = time_to_island
            
            if best_island is None:
                break  # No more islands reachable within time budget
            
            # Add best island to trip
            trip_plan.extend(best_path[1:])  # Skip current location
            visited_this_trip.add(best_island)
            current_location = best_island
            remaining_time -= best_time
        
        # Return to starting island
        if current_location != self.starting_island:
            return_path, return_time = self.find_shortest_path(current_location, self.starting_island)
            if return_time <= remaining_time:
                trip_plan.extend(return_path[1:])
        
        return trip_plan
    
    def execute_trip(self, trip_plan: List[str]):
        """Execute a planned trip and update visit records"""
        print(f"Knowledge sharing trip: {' -> '.join(trip_plan)}")
        
        total_time = 0
        for i in range(len(trip_plan) - 1):
            from_island = trip_plan[i]
            to_island = trip_plan[i + 1]
            if to_island in self.graph.routes[from_island]:
                travel_time = self.graph.routes[from_island][to_island]
                total_time += travel_time
                print(f"  Travel: {from_island} -> {to_island} ({travel_time} days)")
        
        # Update visit records
        current_time = 0
        for i in range(len(trip_plan)):
            island_name = trip_plan[i]
            
            if i > 0:  # Calculate time when we arrive at each island
                from_island = trip_plan[i-1]
                travel_time = self.graph.routes[from_island][island_name]
                current_time += travel_time

            # Skip the starting island on the first visit, but update when returning
            if not (island_name == self.starting_island and i == 0):
                island = self.graph.islands[island_name]
                island.last_visited = current_time
                island.visit_count += 1
                print(f"  Visited {island_name} (pop: {island.population:,})")

        
        print(f"  Total trip time: {total_time} days")
        return total_time
        
# -------------------------------
# PERSON 2 - Eric Chae
# ICS 311 Assignment: Polynesian Triangle
# This class implements a resource distribution algorithm that uses Dijkstra’s algorithm
# -------------------------------

class ResourceDistributor:
    """
    Handles efficient distribution of a resource produced in only one island.
    Each canoe can only carry one unit, and we assume limited canoes per trip.
    """

    def __init__(self, graph: PolynesianGraph, resource_name: str, origin_island: str, total_units: int):
        self.graph = graph
        self.resource_name = resource_name  # Resource to distribute (e.g., shells)
        self.origin_island = origin_island  # Where the resource originates
        self.total_units = total_units      # Total supply available

    def dijkstra_all_paths(self, start: str) -> Dict[str, Tuple[int, List[str]]]:
        """
        Computes shortest paths from start to all reachable islands using Dijkstra's.
        Returns a dictionary: island -> (time, path)
        """
        heap = [(0, start, [])]  # (travel_time, island, path)
        distances = {}  # Final shortest paths and times

        while heap:
            time, node, path = heapq.heappop(heap)
            if node in distances:
                continue  # Already finalized
            distances[node] = (time, path + [node])
            for neighbor, t in self.graph.get_neighbors(node):
                if neighbor not in distances:
                    heapq.heappush(heap, (time + t, neighbor, path + [node]))

        return distances

    def distribute_resources(self, canoe_capacity: int = 1) -> List[Tuple[str, int, List[str]]]:
        """
        Distribute one unit to each island from the origin.
        Returns list of (island, trips_needed, route)
        """
        distances = self.dijkstra_all_paths(self.origin_island)
        results = []

        for island_name, (time, path) in distances.items():
            if island_name == self.origin_island:
                continue  # Skip the origin
            demand = 1
            trips_needed = -(-demand // canoe_capacity)  # Ceiling division
            results.append((island_name, trips_needed, path))

        return sorted(results, key=lambda x: x[1])  # Sort by trips needed
