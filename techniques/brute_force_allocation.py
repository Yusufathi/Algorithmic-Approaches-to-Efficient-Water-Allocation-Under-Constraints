from .allocation_technique import AllocationTechnique
from itertools import product

class BruteForceAllocation(AllocationTechnique):
    """
    Brute force approach for water allocation.
    """

    def allocate(self, water_supply, demands, pipeline_losses):
        regions = list(demands.keys())
        
        max_allocation = {region: min(demands[region], water_supply) for region in regions}
        
        step_size = 5
        
        allocation_ranges = {
            region: range(0, max_allocation[region] + 1, step_size)
            for region in regions
        }
        
        all_combinations = product(*allocation_ranges.values())
        
        best_allocation = {}
        max_efficiency = float('-inf')
        
        for combination in all_combinations:
            allocation = dict(zip(regions, combination))
            
            actual_allocation = {
                region: allocation[region] * (1 - pipeline_losses[region])
                for region in regions
            }
            total_allocated = sum(actual_allocation.values())
            
            if total_allocated > water_supply:
                continue
            
            total_losses = sum(
                allocation[region] * pipeline_losses[region]
                for region in regions
            )
            
            utilization_efficiency = total_allocated / water_supply
            loss_efficiency = 1 - (total_losses / water_supply)
            fairness_index = sum(
                (actual_allocation[region] / demands[region]) if demands[region] else 0
                for region in regions
            ) / len(regions)
            
            overall_efficiency = (
                0.4 * utilization_efficiency +
                0.4 * loss_efficiency +
                0.2 * fairness_index
            )
            
            if overall_efficiency > max_efficiency:
                max_efficiency = overall_efficiency
                best_allocation = {region: actual_allocation[region] for region in regions}
        
        return best_allocation

