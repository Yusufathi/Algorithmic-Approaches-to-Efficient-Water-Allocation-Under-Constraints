from collections import defaultdict, deque

def ford_fulkerson_allocate(water_supply, demands, pipeline_losses, weights):
    """
    Allocate water using the Ford-Fulkerson algorithm.

    Args:
        water_supply (int): Total available water supply.
        demands (dict): Dictionary with region names as keys and their water demands as values.
        pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.
        weights (list): Weights for utilization, loss efficiency, and fairness.

    Returns:
        dict: Allocation for each region and efficiency metrics.
    """
    # Handle edge cases
    if water_supply == 0:
        return {**{region: 0 for region in demands}, "util": 0, "loss": 1, "fairness": 0, "overall": 0}
    if all(demand == 0 for demand in demands.values()):
        return {**{region: 0 for region in demands}, "util": 0, "loss": 0, "fairness": 1, "overall": 0}
    if all(pipeline_losses.get(region, 0) == 1 for region in demands):
        return {**{region: 0 for region in demands}, "util": 0, "loss": 1, "fairness": 0, "overall": 0}

    # Build the graph
    graph = defaultdict(dict)
    source = "source"
    sink = "sink"
    for region, demand in demands.items():
        effective_capacity = int(demand / (1 - pipeline_losses.get(region, 0)))
        graph[source][region] = min(effective_capacity, water_supply)
        graph[region][sink] = demand

    # Run Ford-Fulkerson
    max_flow, flow_network = ford_fulkerson(graph, source, sink)

    # Allocation logic
    allocation = {}
    total_allocated = 0
    total_losses = 0
    fairness_sum = 0
    remaining_supply = water_supply

    for region, demand_value in demands.items():
        allocated_flow = min(flow_network[source].get(region, 0), remaining_supply)
        actual_allocation = int(allocated_flow * (1 - pipeline_losses.get(region, 0)))
        allocation[region] = min(actual_allocation, remaining_supply)
        remaining_supply -= allocation[region]
        total_allocated += allocation[region]
        total_losses += allocated_flow * pipeline_losses.get(region, 0)
        if demand_value > 0:
            fairness_sum += allocation[region] / demand_value

    # Metrics
    utilization = min(total_allocated / water_supply, 1)
    loss = 1 - (total_losses / water_supply)
    fairness = fairness_sum / len([region for region in demands if demands[region] > 0])

    # Overall efficiency
    w1, w2, w3 = weights
    overall_efficiency = (w1 * utilization) + (w2 * loss) + (w3 * fairness)

    # Return results
    return {**allocation, "util": round(utilization, 2), "loss": round(loss, 2), "fairness": round(fairness, 2), "overall": round(overall_efficiency, 2)}


def ford_fulkerson(graph, source, sink):
    """
    Implements the Ford-Fulkerson Algorithm for maximum flow.

    Args:
        graph (dict): Original graph represented as an adjacency list with capacities.
        source (str): Source node.
        sink (str): Sink node.

    Returns:
        tuple: (max_flow, flow_network), where:
            max_flow (int): The maximum flow from source to sink.
            flow_network (dict): The flow network representing flows between nodes.
    """
    # Initialize residual graph
    residual_graph = {u: dict(v) for u, v in graph.items()}
    for u in graph:
        for v in graph[u]:
            if v not in residual_graph:
                residual_graph[v] = {}
            if u not in residual_graph[v]:
                residual_graph[v][u] = 0

    # Initialize flow network
    flow_network = {u: {v: 0 for v in graph[u]} for u in graph}
    for u in graph:
        for v in graph[u]:
            if v not in flow_network:
                flow_network[v] = {}
            if u not in flow_network[v]:
                flow_network[v][u] = 0

    max_flow = 0

    # Find augmenting paths
    while True:
        parent_map = bfs(residual_graph, source, sink)
        if not parent_map:
            break

        # Find bottleneck capacity
        bottleneck = float("Inf")
        v = sink
        while v != source:
            u = parent_map[v]
            bottleneck = min(bottleneck, residual_graph[u][v])
            v = u

        # Update flows and residual graph
        v = sink
        while v != source:
            u = parent_map[v]
            flow_network[u][v] += bottleneck
            flow_network[v][u] -= bottleneck
            residual_graph[u][v] -= bottleneck
            residual_graph[v][u] += bottleneck
            v = u

        max_flow += bottleneck

    return max_flow, flow_network


def bfs(residual_graph, source, sink):
    """
    Performs BFS on the residual graph to find an augmenting path.

    Args:
        residual_graph (dict): Residual graph with remaining capacities.
        source (str): Source node.
        sink (str): Sink node.

    Returns:
        dict or None: A parent map if a path is found, otherwise None.
    """
    visited = set()
    parent_map = {}
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v, capacity in residual_graph[u].items():
            if v not in visited and capacity > 0:  # Only consider edges with remaining capacity
                visited.add(v)
                parent_map[v] = u
                if v == sink:
                    return parent_map  # Path to sink found
                queue.append(v)
    return None


# Example test case
if __name__ == "__main__":
    test_case = {
        "name": "Test Case 1: Simple Allocation",
        "water_supply": 1000,
        "demands": {
            "R1": 400,
            "R2": 300,
            "R3": 500
        },
        "pipeline_losses": {
            "R1": 0.05,
            "R2": 0.03,
            "R3": 0.07
        },
        "expected_output": {
            "R1": 380,
            "R2": 290,
            "R3": 330
        }
    }

    weights = [0.4, 0.4, 0.2]  # Example weights for metrics
    allocation = ford_fulkerson_allocate(
        test_case["water_supply"],
        test_case["demands"],
        test_case["pipeline_losses"],
        weights
    )
    print("Final Allocation:", allocation)
