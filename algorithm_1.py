import heapq
from typing import List, Tuple
from islands_graph import PolynesianGraph, create_polynesian_graph

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
