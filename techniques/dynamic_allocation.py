from .allocation_technique import AllocationTechnique

class DynamicProgrammingAllocation(AllocationTechnique):
    """
    Dynamic programming approach for water allocation.
    """

    def allocate(self, water_supply, demands, pipeline_losses, weights):
        """
        Abstract method to allocate water.

        Args:
            water_supply (int): Total available water supply.
            demands (dict): Dictionary with region names as keys and their water demands as values.
                            Example: {"R1": 400, "R2": 300, "R3": 500}
            pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.
                                    Example: {"R1": 0.05, "R2": 0.03, "R3": 0.07}

        Returns:
            dict: Allocation of water to each region after considering demands and pipeline losses.
                Example Output:
                {
                    "R1": 380,
                    "R2": 290,
                    "R3": 330,
                    'util': 0.95,
                    'loss': 0.59,
                    'fairness': 0.80,
                    'overall': 0.9

                }
        """
        allocations = {}
        adjusted_demands = {}
        for demand, loss in zip(demands, pipeline_losses):
            if (pipeline_losses[demand] == 1.0):
                allocations[demand] = 0
                continue
            adjusted_demands[demand] = demands[demand] + (demands[demand] * pipeline_losses[loss])

        total_adjusted_demand = 0
        for demand in adjusted_demands:
            total_adjusted_demand += adjusted_demands[demand]

        # supplying based on whether we have excess water or not
        if (water_supply > total_adjusted_demand):
            for adj_demand in adjusted_demands:
                allocations[adj_demand] = adjusted_demands[adj_demand]

        else:
            for adj_demand in adjusted_demands:
                allocations[adj_demand] = water_supply * (adjusted_demands[adj_demand] / total_adjusted_demand)

        # currently, the allocations stores the water supply SENT to the region, 
        # the following section adjusts the allocations to show the final water supply RECEIVED by the region after pipeline loss
        for i in (allocations):
            if (allocations[i] == 0):
                continue
            allocations[i] = round(allocations[i] - (demands[i] * pipeline_losses[i]), 2)

        loss_ratio = {}
        for i in (allocations):
            if (allocations[i] == 0):
                loss_ratio[i] = 0
                continue
            loss_ratio[i] = (allocations[i] / demands[i])
            
        return allocations
