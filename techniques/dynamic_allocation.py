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
        pass
