import random
import math

def create_population(size, puzzle, n):
    """Generate a population of random Sudoku boards."""
    population = []
    for _ in range(size):
        individual = [[puzzle[row][col] if puzzle[row][col] != 0 else random.randint(1, n) for col in range(n)] for row in range(n)]
        population.append(individual)
    return population

def fitness(individual, n):
    """Calculate the fitness of the Sudoku board."""
    score = 0
    subgrid_size = int(math.sqrt(n))
    
    # Row and Column Uniqueness
    for i in range(n):
        row_unique = len(set(individual[i]))  # Unique numbers in the row
        col_unique = len(set([individual[j][i] for j in range(n)]))  # Unique numbers in the column
        score += row_unique + col_unique

    # Subgrid Uniqueness
    for row in range(0, n, subgrid_size):
        for col in range(0, n, subgrid_size):
            subgrid = [individual[r][c] for r in range(row, row + subgrid_size) for c in range(col, col + subgrid_size)]
            subgrid_unique = len(set(subgrid))  # Unique numbers in the subgrid
            score += subgrid_unique

    return score

def mutate(individual, puzzle, n, mutation_rate=0.70):
    """Apply random mutation to an individual."""
    for _ in range(int(mutation_rate * n * n)):  
        row = random.randint(0, n-1)
        col = random.randint(0, n-1)

        # Only mutate empty cells
        if puzzle[row][col] == 0:
            individual[row][col] = random.randint(1, n)

    return individual

def crossover(parent1, parent2, n):
    """Perform crossover between two parents."""
    child = []
    for row in range(n):
        if random.random() < 0.5:
            child.append(parent1[row][:])
        else:
            child.append(parent2[row][:])
    return child

def genetic_algorithm(puzzle, n=9, population_size=200, generations=2000):
    """Solve Sudoku using a Genetic Algorithm."""
    population = create_population(population_size, puzzle, n)
    
    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x, n), reverse=True)

        # If a perfect solution is found
        if fitness(population[0], n) == n * n * 3:
            return population[0]

        # Create the next generation
        next_generation = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(population[:10], 2)
            child1 = crossover(parent1, parent2, n)
            child2 = crossover(parent2, parent1, n)
            next_generation.extend([mutate(child1, puzzle, n), mutate(child2, puzzle, n)])

        population = next_generation

    return None  # No perfect solution found
