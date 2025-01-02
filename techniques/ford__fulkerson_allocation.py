from .allocation_technique import AllocationTechnique
from collections import defaultdict, deque

class FordFulkersonAllocation(AllocationTechnique):
    """
    Greedy approach for water allocation Using Ford-Fulkerson Algorithm
    """

    def allocate(self, water_supply, demands, pipeline_losses):
        """
        Allocate water using the Ford-Fulkerson algorithm.

        Args:
            water_supply (int): Total available water supply.
            demands (dict): Dictionary with region names as keys and their water demands as values.
                            Example: {"R1": 400, "R2": 300, "R3": 500}
            pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.
                                    Example: {"R1": 0.05, "R2": 0.03, "R3": 0.07}

        Returns:
            dict: Allocation of water to each region after considering demands and pipeline losses.
        """
        graph = defaultdict(dict)
        source = "source"
        sink = "sink"
        for region, demand in demands.items():
            if region in pipeline_losses:
                effective_capacity = int(demand / (1 - pipeline_losses[region]))
            else:
                effective_capacity = demand
            graph[source][region] = min(effective_capacity, water_supply)
        for region, demand in demands.items():
            graph[region][sink] = demand
        max_flow, flow_network = self._ford_fulkerson(graph, source, sink)
        allocation = {}
        for region in demands.keys():
            allocated_flow = flow_network[source].get(region, 0)
            allocation[region] = int(allocated_flow * (1 - pipeline_losses.get(region, 0)))

        return allocation




    def _ford_fulkerson(self, graph, source, sink):
        """
        Implements the Ford-Fulkerson Algorithm for maximum flow.
        """
        residual_graph = {u: dict(v) for u, v in graph.items()}
        for u in graph:
            for v in graph[u]:
                if v not in residual_graph:
                    residual_graph[v] = {}
                if u not in residual_graph[v]:
                    residual_graph[v][u] = 0
        flow_network = {u: {v: 0 for v in graph[u]} for u in graph}
        for u in graph:
            for v in graph[u]:
                if v not in flow_network:
                    flow_network[v] = {}
                if u not in flow_network[v]:
                    flow_network[v][u] = 0

        max_flow = 0

        while True:
            parent_map = self._bfs(residual_graph, source, sink)
            if not parent_map:
                break  
            bottleneck = float("Inf")
            v = sink
            while v != source:
                u = parent_map[v]
                bottleneck = min(bottleneck, residual_graph[u][v])
                v = u
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



    def _bfs(self, residual_graph, source, sink):
        """
        Performs BFS on the residual graph to find an augmenting path.
        """
        if source not in residual_graph:
            raise KeyError(f"Source node '{source}' not found in the residual graph.")

        visited = set()
        parent_map = {}
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v, capacity in residual_graph[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent_map[v] = u
                    if v == sink:
                        return parent_map
                    queue.append(v)
        return None
