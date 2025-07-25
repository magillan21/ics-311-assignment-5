# main.py
from algorithms import PolynesianGraph, ResourceDistributor, KnowledgeShareLeader
from polynesian_triangle import create_polynesian_graph

def test_knowledge_share():
    """
    Test the KnowledgeShareLeader class by planning and executing a trip
    that visits high-priority islands within a limited time.
    """
    print("=== Testing Knowledge Sharing ===")
    
    # Create the graph of islands and routes
    graph = create_polynesian_graph()
    
    # Initialize the knowledge sharing leader at Hawaii
    leader = KnowledgeShareLeader(graph, starting_island="Hawaii")
    
    # Define the maximum number of days allowed for the trip
    max_trip_time = 60

    # Plan the trip based on priorities and travel constraints
    trip_plan = leader.plan_knowledge_sharing_trip(max_trip_time)
    print(f"Planned trip (max {max_trip_time} days):", trip_plan)

    # Execute the trip and update visit times
    leader.execute_trip(trip_plan)

    # Print out last visited time for each island in the trip
    unique_islands = list(set(trip_plan))  # Remove duplicates
    for island_name in unique_islands:
        island = graph.islands[island_name]
        print(f"{island_name}: Last visited on day {island.last_visited}, total visits: {island.visit_count}")


def test_resource_distribution():
    """
    Test the ResourceDistributor class by distributing a resource
    from one origin island to all others.
    """
    print("\n=== Testing Resource Distribution ===")

    # Create the graph of islands and routes
    graph = create_polynesian_graph()

    # Initialize distributor for "shells" starting from Hawaii
    distributor = ResourceDistributor(
        graph, resource_name="shells", origin_island="Hawaii", total_units=10
    )

    # Distribute shells using 1 unit per canoe trip
    results = distributor.distribute_resources(canoe_capacity=1)

    # Output number of trips and routes for each island
    for island, trips_needed, route in results:
        print(f"{island}: {trips_needed} trip(s) needed, route: {route}")


if __name__ == "__main__":
    # test_knowledge_share()  # <-- Currently commented out
    test_resource_distribution()
