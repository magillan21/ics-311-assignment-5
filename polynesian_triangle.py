from collections import defaultdict
from typing import Dict, List, Tuple, Optional
__all__ = ['PolynesianGraph', 'create_polynesian_graph', 'KnowledgeShareLeader', 'ResourceDistributor']


class Island:
    """Represents a single island with its properties"""
    def __init__(self, name: str, population: int, resources: Dict[str, int] = None):
        self.name = name
        self.population = population
        self.resources = resources or {}
        self.last_visited = 0  # Timestamp of last leader visit
        self.visit_count = 0
    
    def __repr__(self):
        return f"Island({self.name}, pop={self.population})"

class PolynesianGraph:
    """Represents the islands as a weighted graph"""
    def __init__(self):
        self.islands: Dict[str, Island] = {}
        self.routes: Dict[str, Dict[str, int]] = defaultdict(dict)  # adjacency list
        
    def add_island(self, name: str, population: int, resources: Dict[str, int] = None):
        """Add an island to the graph"""
        self.islands[name] = Island(name, population, resources)
    
    def add_route(self, from_island: str, to_island: str, travel_time: int):
        """Add a directed route between islands"""
        if from_island not in self.islands or to_island not in self.islands:
            raise ValueError("Both islands must exist before adding route")
        self.routes[from_island][to_island] = travel_time
    
    def get_neighbors(self, island: str) -> List[Tuple[str, int]]:
        """Get all islands reachable from given island with travel times"""
        if island not in self.routes:
            return []
        return [(neighbor, time) for neighbor, time in self.routes[island].items()]
    
    def get_island_names(self) -> List[str]:
        """Get all island names"""
        return list(self.islands.keys())

def create_polynesian_graph() -> PolynesianGraph:
    """Create the shared graph with 5 islands and 3 resource types"""
    graph = PolynesianGraph()
    
    # Add 5 islands with populations and 3 resource types
    islands_data = [
        ("New_Zealand", 5000000, {"shells": 20, "sweet_potato": 90, "kava": 40}),
        ("Hawaii", 1400000, {"shells": 100, "sweet_potato": 100, "kava": 30}),
        ("Tahiti", 275000, {"shells": 50, "sweet_potato": 80, "kava": 150}),
        ("Samoa", 200000, {"shells": 40, "sweet_potato": 70, "kava": 180}),
        ("Easter_Island", 8000, {"shells": 10, "sweet_potato": 150, "kava": 5}),
    ]
    
    for name, population, resources in islands_data:
        graph.add_island(name, population, resources)
    
    # Add routes (travel times in days, asymmetric)
    routes = [
        ("Hawaii", "Tahiti", 15),
        ("Tahiti", "Hawaii", 18),
        ("Tahiti", "Samoa", 8),
        ("Samoa", "Tahiti", 10),
        ("Samoa", "New_Zealand", 12),
        ("New_Zealand", "Samoa", 14),
        ("Easter_Island", "Tahiti", 20),
        ("Tahiti", "Easter_Island", 22),
        ("Hawaii", "Samoa", 20),
        ("Samoa", "Hawaii", 18),
        ("New_Zealand", "Tahiti", 16),
        ("Tahiti", "New_Zealand", 18),
    ]
    
    for from_island, to_island, time in routes:
        graph.add_route(from_island, to_island, time)
    
    
    return graph
