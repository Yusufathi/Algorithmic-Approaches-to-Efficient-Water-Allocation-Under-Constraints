from .allocation_technique import AllocationTechnique

class DynamicProgrammingAllocation(AllocationTechnique):
    """
    Dynamic programming approach for water allocation.
    """

    def allocate(self, water_supply, demands, pipeline_losses):
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
                    "R3": 330
                }
        """
        
        adjusted_demands = {}
        for demand, loss in zip(demands, pipeline_losses):
            adjusted_demands[demand] = demands[demand] + (demands[demand] * pipeline_losses[loss])
        print("Adjusted Demands: ",adjusted_demands)

        total_adjusted_demand = 0
        for demand in adjusted_demands:
            total_adjusted_demand += adjusted_demands[demand]
        print("Total Adjusted Demand: ", total_adjusted_demand)

        allocations = {}
        for adj_demand in adjusted_demands:
            allocations[adj_demand] = water_supply * (adjusted_demands[adj_demand] / total_adjusted_demand)
        print("Allocations: ", allocations)

        loss_ratio = {}
        for i in (allocations):
            loss_ratio[i] = (allocations[i] / demands[i])
        print("Loss Ratio: ", loss_ratio)

        return allocations
        # pass
