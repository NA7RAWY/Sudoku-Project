from genetic_solver import genetic_algorithm


def print_board(board):
    """Helper function to print a Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))
    print()


# Example Sudoku puzzle
puzzle = [
            [1, 0, 0, 4],
            [0, 0, 3, 0],
            [0, 1, 0, 0],
            [3, 0, 0, 2]
        ]

if __name__ == "__main__":
    print("Original Puzzle:")
    print_board(puzzle)

    # Solve using Backtracking Algorithm
    print("Solving with Backtracking Algorithm...")
    puzzle_copy = [row[:] for row in puzzle]  # Copy the puzzle to avoid modifying the original


    # Solve using Genetic Algorithm
print("Solving with Genetic Algorithm...")
solution = genetic_algorithm(puzzle, n=len(puzzle))

if solution:
        print("Solved Puzzle:")
        print_board(solution)
else:
        print("No solution found using Genetic Algorithm.")