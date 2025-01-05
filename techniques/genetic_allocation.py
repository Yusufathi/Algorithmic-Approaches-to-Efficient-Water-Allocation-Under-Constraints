from .allocation_technique import AllocationTechnique

import numpy as np

import numpy as np

class GeneticAlgorithmAllocation(AllocationTechnique):
    """
    Genetic algorithm approach for water allocation.
    """

    def allocate(self, water_supply, demands, pipeline_losses, weights):
        """
        Allocates water to regions using a Genetic Algorithm and calculates specified metrics.

        Args:
            water_supply (int): Total available water supply.
            demands (dict): Dictionary with region names as keys and their water demands as values.
                            Example: {"R1": 400, "R2": 300, "R3": 500}
            pipeline_losses (dict): Dictionary with region names as keys and pipeline loss percentages as values.
                                    Example: {"R1": 0.05, "R2": 0.03, "R3": 0.07}
            weights (tuple): Weights for the overall efficiency calculation (w1, w2, w3).

        Returns:
            dict: Allocation of water to each region after considering demands and pipeline losses,
                  along with calculated metrics.
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
        # Combine demands and pipeline_losses into a single regions dictionary
        regions = {name: {'demand': demands[name], 'loss': pipeline_losses[name]} for name in demands}

        # Calculate required needs considering pipeline losses
        self.calculate_required_needs(regions)

        num_regions = len(regions)
        population_size = 100
        generations = 1000
        mutation_rate = 0.01
        w1, w2, w3 = weights

        # Initialize population with random allocations
        population = self.initialize_population(population_size, num_regions, water_supply)

        # Main Genetic Algorithm loop
        for generation in range(generations):
            fitnesses = [self.fitness(ind, regions) for ind in population]
            population = self.selection(population, fitnesses, population_size)
            next_generation = []
            for i in range(0, population_size, 2):
                parent1, parent2 = population[i], population[i+1]
                child1, child2 = self.crossover(parent1, parent2)
                next_generation.extend([self.mutate(child1, mutation_rate, water_supply),
                                        self.mutate(child2, mutation_rate, water_supply)])
            population = next_generation
            # Optional: Print best fitness every 100 generations
            if generation % 100 == 0:
                print(f'Generation {generation}: Best Fitness = {max(fitnesses)}')

        # Determine the best solution
        best_index = np.argmax([self.fitness(ind, regions) for ind in population])
        best_allocation = population[best_index]

        # Calculate metrics
        total_allocated_water = sum(best_allocation)
        utilization_efficiency = total_allocated_water / water_supply

        total_water_losses = sum(allocation * regions[region_name]['loss']
                                 for allocation, region_name in zip(best_allocation, regions.keys()))
        loss_efficiency = 1 - (total_water_losses / water_supply)

        fairness_index = (1 / num_regions) * sum(
            allocation / regions[region_name]['demand']
            for allocation, region_name in zip(best_allocation, regions.keys())
        )

        overall_efficiency = (w1 * utilization_efficiency) + (w2 * loss_efficiency) + (w3 * fairness_index)

        # Prepare the final result dictionary
        result = {region_name: allocation for allocation, region_name in zip(best_allocation, regions.keys())}
        result.update({
            'util': utilization_efficiency,
            'loss': loss_efficiency,
            'fairness': fairness_index,
            'overall': overall_efficiency
        })

        return result

    def calculate_required_needs(self, regions):
        for region in regions.values():
            region['required_need'] = region['demand'] + (region['demand'] * region['loss'])

    def initialize_population(self, population_size, num_regions, total_supply):
        return [np.random.dirichlet(np.ones(num_regions)) * total_supply for _ in range(population_size)]

    def fitness(self, individual, regions):
        percentages = []
        for allocation, region in zip(individual, regions.values()):
            received_water = allocation * (1 - region['loss'])
            percentage_met = received_water / region['demand']
            percentages.append(percentage_met)
        return -np.var(percentages)

    def selection(self, population, fitnesses, population_size):
        selected = []
        for _ in range(population_size):
            i, j = np.random.randint(0, population_size, 2)
            selected.append(population[i] if fitnesses[i] > fitnesses[j] else population[j])
        return selected

    def crossover(self, parent1, parent2):
        point = np.random.randint(1, len(parent1))
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2

    def mutate(self, individual, mutation_rate, total_supply):
        if np.random.rand() < mutation_rate:
            idx = np.random.randint(len(individual))
            individual[idx] = np.random.uniform(0, total_supply)
            # Normalize to ensure total allocation doesn't exceed total_supply
            individual = individual / np.sum(individual) * total_supply
        return individual
