from backtracking_solver import solve_sudoku as solve_with_backtracking, is_valid
from genetic_solver import genetic_algorithm
import random

def display_menu():
    """Display the main menu for user interaction."""
    print("\nWelcome to the Sudoku Solver!")
    print("1. Input your own sudoku puzzle")
    print("2. Select a predefined Sudoku puzzle")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ").strip()
    return choice

def display_algorithm_menu():
    """Display the menu for algorithm selection."""
    print("\nSelect the algorithm to solve the Sudoku:")
    print("1. Solve with Backtracking Algorithm")
    print("2. Solve with Genetic Algorithm")
    choice = input("Enter your choice (1/2): ").strip()
    return choice

def get_grid_size():
    """Prompt the user to enter the Sudoku grid size."""
    while True:
        try:
            grid_size = int(input("Enter the Sudoku grid size (4, 6, 9): "))
            if grid_size in [4, 6, 9]:
                return grid_size
            else:
                print("Invalid grid size. Please choose 4, 6, or 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_subgrid_dimensions(grid_size):
    """Determine subgrid dimensions based on grid size."""
    if grid_size == 4:
        return 2, 2
    elif grid_size == 6:
        return 3, 2
    elif grid_size == 9:
        return 3, 3

def print_board(board):
    """Helper function to print a Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))
    print()

def get_sudoku_input(n):
    """Allow users to input a Sudoku puzzle with validation."""
    print(f"Please enter a {n}x{n} Sudoku puzzle (use 0 for empty cells):")
    board = []
    for i in range(n):
        while True:
            try:
                row = list(map(int, input(f"Enter row {i + 1}: ").split()))
                if len(row) != n:
                    raise ValueError(f"Row must have exactly {n} numbers.")
                if not all(0 <= num <= n for num in row):
                    raise ValueError(f"Numbers must be between 0 and {n}.")
                board.append(row)
                break
            except ValueError as e:
                print(e)
    return board

def select_puzzle(n):
    """Select from predefined Sudoku puzzles."""
    if n == 4:
        return [
            [1, 0, 0, 4],
            [0, 0, 3, 0],
            [0, 1, 0, 0],
            [3, 0, 0, 2]
        ]
    elif n == 6:
        return [
            [0, 0, 0, 0, 3, 0],
            [0, 0, 0, 5, 0, 0],
            [0, 0, 0, 0, 0, 4],
            [5, 0, 0, 4, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [4, 0, 3, 0, 0, 0]
        ]
    elif n == 9:
        return [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == "3":  # Exit
            print("Thank you for using the Sudoku Solver. Goodbye!")
            break

        elif choice in ["1", "2"]:  # Custom or Predefined Puzzle
            grid_size = get_grid_size()
            subgrid_rows, subgrid_cols = get_subgrid_dimensions(grid_size)

            if choice == "1":
                puzzle = get_sudoku_input(grid_size)
            else:
                puzzle = select_puzzle(grid_size)

            print("\nOriginal Puzzle:")
            print_board(puzzle)

            # Algorithm selection
            algorithm_choice = display_algorithm_menu()
            if algorithm_choice == "1":
                print("Solving with Backtracking Algorithm...")
                puzzle_copy = [row[:] for row in puzzle]  # Copy the puzzle to avoid modifying the original
                if solve_with_backtracking(puzzle_copy, subgrid_rows, subgrid_cols):
                    print("\nSolved Puzzle:")
                    print_board(puzzle_copy)
                else:
                    print("No solution exists for the given puzzle.")

            elif algorithm_choice == "2":
                print("Solving with Genetic Algorithm...")
                solution = genetic_algorithm(puzzle, n=grid_size)
                if solution:
                    print("\nSolved Puzzle:")
                    print_board(solution)
                else:
                    print("No solution found using Genetic Algorithm.")
            else:
                print("Invalid choice. Please select 1 or 2.")
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
