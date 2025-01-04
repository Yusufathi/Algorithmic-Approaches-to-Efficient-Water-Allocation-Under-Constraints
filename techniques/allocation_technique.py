from abc import ABC, abstractmethod

class AllocationTechnique(ABC):
    """
    Abstract base class for water allocation techniques.
    """

    @abstractmethod
    def allocate(self, water_supply, demands, pipeline_losses,weights):
        """
        Abstract method to allocate water.

        Args:
            water_supply (int): Total available water supply.
            demands (dict): Dictionary with region names as keys and their demands as values.
            pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.

        Returns:
            dict: Allocation of water to each region.
            dict: for all the effiency metrics we have. eg, metrics : { 'util': 0.95, 'loss': 0.59, 'fairness': 0.80, 'overall': 0.9}
        """
        pass
