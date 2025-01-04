from .allocation_technique import AllocationTechnique
from itertools import product
from tqdm import tqdm


class BruteForceAllocation(AllocationTechnique):
    """
    Brute force approach for water allocation.
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
        is_progress_indicator_enabled = True
        regions = list(demands.keys())
        
        max_allocation = {region: min(demands[region], water_supply) for region in regions}
        step_size = 5
        
        allocation_ranges = {
            region: range(0, max_allocation[region] + 1, step_size)
            for region in regions
        }
        
        all_combinations = product(*allocation_ranges.values())
        total_combinations = 1
        for region in allocation_ranges:
            total_combinations *= len(allocation_ranges[region])
        
        best_allocation = {}
        max_efficiency = float('-inf')
        
        if is_progress_indicator_enabled:
            with tqdm(total=total_combinations, desc="Brute Force Progress") as progress:
                for combination in all_combinations:
                    allocation = dict(zip(regions, combination))
                    
                    actual_allocation = {
                        region: allocation[region] * (1 - pipeline_losses[region])
                        for region in regions
                    }
                    total_allocated = sum(actual_allocation.values())
                    
                    if total_allocated > water_supply:
                        progress.update(1)
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
                        weights[0] * utilization_efficiency +
                        weights[1] * loss_efficiency +
                        weights[2] * fairness_index
                    )
                    
                    if overall_efficiency > max_efficiency:
                        max_efficiency = overall_efficiency
                        best_allocation = {region: round(actual_allocation[region], 2) for region in regions}
                    
                    progress.update(1)
        
        # Calculate metrics for the best allocation
        total_losses = sum(
            best_allocation[region] * pipeline_losses[region] for region in regions
        )
        total_allocated = sum(best_allocation.values())
        utilization_efficiency = total_allocated / water_supply
        loss_efficiency = 1 - (total_losses / water_supply)
        fairness_index = sum(
            (best_allocation[region] / demands[region]) if demands[region] else 0
            for region in regions
        ) / len(regions)
        overall_efficiency = (
            weights[0] * utilization_efficiency +
            weights[1] * loss_efficiency +
            weights[2] * fairness_index
        )
        
        return {
            **best_allocation,
            "util": round(utilization_efficiency, 2),
            "loss": round(loss_efficiency, 2),
            "fairness": round(fairness_index, 2),
            "overall": round(overall_efficiency, 2)
        }

