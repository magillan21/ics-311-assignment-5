# Import classes and function from your polynesian_triangle.py
from polynesian_triangle import PolynesianGraph, create_polynesian_graph, KnowledgeShareLeader, ResourceDistributor

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
    for island_name in trip_plan:
        island = graph.islands[island_name]
        print(f"{island_name}: Last visited at time {island.last_visited}")

def test_resource_distribution():
    """
    Test the ResourceDistributor class by distributing a resource
    from one origin island to all others.
    """
    print("\n=== Testing Resource Distribution ===")

    # Create the same graph of islands and routes
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
    # Run both tests when the script is executed directly
    test_knowledge_share()
    test_resource_distribution()
