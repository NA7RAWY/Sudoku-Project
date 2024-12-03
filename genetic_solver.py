import random
import math

def create_population(size, puzzle, n):
    """Generate a population of random Sudoku boards."""
    population = []
    for _ in range(size):
        individual = [[puzzle[row][col] if puzzle[row][col] != 0 else random.randint(1, n) for col in range(n)] for row in range(n)]
        population.append(individual)
    return population

def print_board(board):
    """Helper function to print a Sudoku board."""
    n = len(board)
    subgrid_size = int(math.sqrt(n))
    for row in range(n):
        print(" ".join(str(num) if num != 0 else '.' for num in row))
        if (row + 1) % subgrid_size == 0:
            print()

def fitness(individual, n):
    """Calculate the fitness of the Sudoku board."""
    score = 0
    subgrid_height, subgrid_width = get_subgrid_size(n)
    
    # Row and Column Uniqueness
    for i in range(n):
        row_unique = len(set(individual[i]))  # Unique numbers in the row
        col_unique = len(set([individual[j][i] for j in range(n)]))  # Unique numbers in the column
        score += row_unique + col_unique

    # Subgrid Uniqueness
    for row in range(0, n, subgrid_height):
        for col in range(0, n, subgrid_width):
            subgrid = [individual[r][c] for r in range(row, row + subgrid_height) 
                       for c in range(col, col + subgrid_width)]
            subgrid_unique = len(set(subgrid))  # Unique numbers in the subgrid
            score += subgrid_unique

    return score



def mutate(individual, puzzle, n, mutation_rate=0.35):
    """Apply random mutation to an individual."""
    subgrid_height, subgrid_width = get_subgrid_size(n)
    
    for _ in range(int(mutation_rate * n * n)):
        row = random.randint(0, n-1)
        col = random.randint(0, n-1)

        if puzzle[row][col] == 0:  # Only mutate empty cells
            current_values = set(individual[row]) | \
                            set([individual[i][col] for i in range(n)]) | \
                            set([individual[r][c] 
                                for r in range(row // subgrid_height * subgrid_height, 
                                                (row // subgrid_height + 1) * subgrid_height) 
                                for c in range(col // subgrid_width * subgrid_width, 
                                                (col // subgrid_width + 1) * subgrid_width)])
            available_values = [num for num in range(1, n+1) if num not in current_values]
            if available_values:
                individual[row][col] = random.choice(available_values)

        
        # Additional swap logic for exploration
        if random.random() < 0.1:
            row2 = random.randint(0, n-1)
            col2 = random.randint(0, n-1)
            if (row != row2 or col != col2):
                individual[row][col], individual[row2][col2] = individual[row2][col2], individual[row][col]
    return individual


def crossover(parent1, parent2, n):
    """Perform crossover between two parents."""
    child = []
    subgrid_size = int(math.sqrt(n))
    for row in range(n):
        # Randomly choose rows from either parent
        if random.random() < 0.5:
            child.append(parent1[row][:])
        else:
            child.append(parent2[row][:])

    # Ensure subgrids are consistent after crossover
    for row in range(0, n, subgrid_size):
        for col in range(0, n, subgrid_size):
            subgrid = [child[r][c] for r in range(row, row + subgrid_size) for c in range(col, col + subgrid_size)]
            unique_numbers = set(subgrid)
            missing_numbers = [n for n in range(1, n+1) if n not in unique_numbers]
            
            if len(unique_numbers) == n:
                # Subgrid is already valid, skip adjustment
                continue
            
            for r in range(row, row + subgrid_size):
                for c in range(col, col + subgrid_size):
                    if subgrid.count(child[r][c]) > 1:  # Replace duplicates
                        if missing_numbers:
                            child[r][c] = missing_numbers.pop(0)
    return child

def genetic_algorithm(puzzle, n, population_size=100, generations=1000):
    """Solve Sudoku using a Genetic Algorithm."""
    population = create_population(population_size, puzzle, n)
    
    best_fitness = 0
    for generation in range(generations):
        # Sort population by fitness (higher is better)
        population = sorted(population, key=lambda x: fitness(x, n), reverse=True)

        # Display the fitness score of the best individual in this generation
        current_fitness = fitness(population[0], n)
        print(f"Generation {generation + 1}: Best Fitness = {current_fitness}")
        
        # Track the best fitness across generations
        if current_fitness > best_fitness:
            best_fitness = current_fitness
        
        # Check if we have a perfect solution (fitness == n * n)
        if current_fitness == 3 * n * n:  # Perfect fitness score
            print("Found perfect solution!")
            return population[0], generation + 1

        # Create the next generation
        next_generation = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(population[:10], 2)  # Select top 10 parents
            child1 = crossover(parent1, parent2, n)
            child2 = crossover(parent2, parent1, n)
            next_generation.extend([mutate(child1, puzzle, n), mutate(child2, puzzle, n)])

        population = next_generation

    # Return the best solution found
    return population[0] if best_fitness == n * n * 3 else None

def get_subgrid_size(n):
    """Return the height and width of subgrids for a given Sudoku size."""
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            subgrid_height, subgrid_width = i, n // i
    return subgrid_height, subgrid_width




