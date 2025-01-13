from .allocation_technique import AllocationTechnique

class ProportionalAllocation(AllocationTechnique):
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
        
        # if water_supply == 0:
        #     return {**{region: 0 for region in demands}, "util": 0, "loss": 1, "fairness": 0, "overall": 0}
        # if all(demand == 0 for demand in demands.values()):
        #     return {**{region: 0 for region in demands}, "util": 0, "loss": 0, "fairness": 1, "overall": 0}
        # if all(pipeline_losses.get(region, 0) == 1 for region in demands):
        #     return {**{region: 0 for region in demands}, "util": 0, "loss": 1, "fairness": 0, "overall": 0}
        
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
        ### Evaluation metrics:
        total_allocated_water = sum(allocations.values())
        utilization_efficiency = total_allocated_water / water_supply
        
        total_water_losses = sum(allocations[region] * pipeline_losses[region] for region in demands)
        loss_efficiency = 1 - (total_water_losses / water_supply)
        # fairness_index = (1 / len(demands)) * sum(allocations[region] / demands[region] for region in demands)
        
        fairness_index = (1 / len(demands)) * sum(
            allocations[region] / demands[region] if demands[region] != 0 else 0
            for region in demands
        )
        
        overall_efficiency = (weights[0] * utilization_efficiency) + (weights[1] * loss_efficiency) + (weights[2] * fairness_index)

        loss_ratio = {}
        for i in (allocations):
            if (allocations[i] == 0):
                loss_ratio[i] = 0
                continue
            loss_ratio[i] = (allocations[i] / demands[i])
            
        return {
                **allocations,
                "util": (utilization_efficiency),
                "loss": (loss_efficiency),
                "fairness": (fairness_index),
                "overall": (overall_efficiency)
                }
