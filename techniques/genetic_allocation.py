from .allocation_technique import AllocationTechnique

class GeneticAlgorithmAllocation(AllocationTechnique):
    """
    Genetic algorithm approach for water allocation.
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
        # Filter out regions with invalid demands or losses
        valid_regions = {name: {'demand': demands[name], 'loss': pipeline_losses[name]}
                         for name in demands
                         if demands[name] > 0 and pipeline_losses[name] < 1}

        if not valid_regions:
            return {**{region: 0 for region in demands}, "util": 0, "loss": 1, "fairness": 0, "overall": 0}

        num_regions = len(valid_regions)
        population_size = 100
        generations = 500
        mutation_rate = 0.05

        # Extract valid demands for valid regions
        valid_demands = np.array([valid_regions[region]['demand'] for region in valid_regions.keys()])

        # Initialize population
        population = self.initialize_population(population_size, num_regions, water_supply, valid_demands)

        for generation in range(generations):
            # Evaluate fitness for all individuals
            fitnesses = [self.fitness(ind, valid_regions, water_supply, weights) for ind in population]
            # Perform selection
            population = self.selection(population, fitnesses, population_size)
            # Generate next generation via crossover and mutation
            next_generation = []
            for i in range(0, population_size, 2):
                parent1, parent2 = population[i], population[i + 1]
                child1, child2 = self.crossover(parent1, parent2, water_supply, valid_demands)
                next_generation.extend([
                    self.mutate(child1, mutation_rate, water_supply, valid_demands),
                    self.mutate(child2, mutation_rate, water_supply, valid_demands)
                ])
            population = next_generation

        # Get the best allocation
        best_index = np.argmax([self.fitness(ind, valid_regions, water_supply, weights) for ind in population])
        best_allocation = population[best_index]

        # Calculate allocations for all regions
        allocations = {
            region_name: round(allocation - (valid_regions[region_name]['demand'] * valid_regions[region_name]['loss']), 2)
            for allocation, region_name in zip(best_allocation, valid_regions.keys())
        }

        # Calculate metrics
        total_allocated_water = sum(best_allocation)
        utilization_efficiency = total_allocated_water / water_supply

        total_water_losses = sum([
            allocation * valid_regions[region_name]['loss']
            for allocation, region_name in zip(best_allocation, valid_regions.keys())
        ])
        loss_efficiency = 1 - (total_water_losses / water_supply)

        fairness_index = (1 / num_regions) * sum(
            min(allocation / valid_regions[region_name]['demand'], 1)
            for allocation, region_name in zip(best_allocation, valid_regions.keys())
        )

        overall_efficiency = (weights[0] * utilization_efficiency) + \
                             (weights[1] * loss_efficiency) + \
                             (weights[2] * fairness_index)

        return {
            **allocations,
            "util": round(utilization_efficiency, 5),
            "loss": round(loss_efficiency, 5),
            "fairness": round(fairness_index, 5),
            "overall": round(overall_efficiency, 5)
        }

    def initialize_population(self, population_size, num_regions, total_supply, valid_demands):
        population = []
        for _ in range(population_size):
            individual = np.random.dirichlet(np.ones(num_regions)) * total_supply
            individual = np.minimum(individual, valid_demands)
            population.append(individual)
        return population

    def fitness(self, individual, regions, total_supply, weights):
        total_allocated_water = np.sum(individual)
        utilization_efficiency = total_allocated_water / total_supply

        total_water_losses = np.sum([
            allocation * regions[region_name]['loss']
            for allocation, region_name in zip(individual, regions.keys())
        ])
        loss_efficiency = 1 - (total_water_losses / total_supply)

        fairness_index = (1 / len(regions)) * sum(
            min(allocation / regions[region_name]['demand'], 1)
            for allocation, region_name in zip(individual, regions.keys())
        )

        overall_efficiency = (weights[0] * utilization_efficiency) + \
                             (weights[1] * loss_efficiency) + \
                             (weights[2] * fairness_index)

        return overall_efficiency

    def selection(self, population, fitnesses, population_size):
        probabilities = np.exp(fitnesses - np.max(fitnesses))
        probabilities /= np.sum(probabilities)
        return [population[np.random.choice(len(population), p=probabilities)] for _ in range(population_size)]

    def crossover(self, parent1, parent2, total_supply, valid_demands):
        point = np.random.randint(1, len(parent1))
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        child1 = np.minimum(child1 / np.sum(child1) * total_supply, valid_demands)
        child2 = np.minimum(child2 / np.sum(child2) * total_supply, valid_demands)
        return child1, child2

    def mutate(self, individual, mutation_rate, total_supply, valid_demands):
        if np.random.rand() < mutation_rate:
            idx = np.random.randint(len(individual))
            max_change = valid_demands[idx] - individual[idx]
            change = np.random.uniform(-individual[idx], max_change)
            individual[idx] += change
            individual = np.minimum(individual / np.sum(individual) * total_supply, valid_demands)
        return individual
