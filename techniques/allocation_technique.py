from abc import ABC, abstractmethod

class AllocationTechnique(ABC):
    """
    Abstract base class for water allocation techniques.
    """

    @abstractmethod
    def allocate(self, water_supply, demands, pipeline_losses):
        """
        Abstract method to allocate water.

        Args:
            water_supply (int): Total available water supply.
            demands (dict): Dictionary with region names as keys and their demands as values.
            pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.

        Returns:
            dict: Allocation of water to each region.
        """
        pass
