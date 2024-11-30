import random


def create_population(size, puzzle):
    """Generate a population of random Sudoku boards."""
    population = []
    for _ in range(size):
        individual = [[puzzle[row][col] if puzzle[row][col] != 0 else random.randint(1, 9) for col in range(9)] for row in range(9)]
        population.append(individual)
    return population


def fitness(individual):
    """Calculate the fitness score of a Sudoku board."""
    score = 0
    for i in range(9):
        score += len(set(individual[i]))  # Unique numbers in rows
        score += len(set([individual[j][i] for j in range(9)]))  # Unique numbers in columns
    return score


def mutate(individual, puzzle):
    """Apply random mutation to an individual."""
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:  # Allow mutation only in empty cells
                if random.random() < 0.1:  # Mutation probability
                    individual[row][col] = random.randint(1, 9)
    return individual


def crossover(parent1, parent2):
    """Perform crossover between two parents."""
    child = []
    for row in range(9):
        if random.random() < 0.5:
            child.append(parent1[row])
        else:
            child.append(parent2[row])
    return child


def genetic_algorithm(puzzle, population_size=100, generations=1000):
    """Solve Sudoku using a Genetic Algorithm."""
    population = create_population(population_size, puzzle)
    for generation in range(generations):
        # Sort population by fitness (higher is better)
        population = sorted(population, key=lambda x: fitness(x), reverse=True)

        # Check if we have a perfect solution
        if fitness(population[0]) == 162:  # Perfect fitness score
            return population[0]

        # Create the next generation
        next_generation = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(population[:10], 2)  # Select top 10 parents
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            next_generation.extend([mutate(child1, puzzle), mutate(child2, puzzle)])

        population = next_generation

    # Return the best solution found
    return None