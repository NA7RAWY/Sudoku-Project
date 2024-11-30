def print_board(board):
    """Helper function to print a Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))
    print()

def is_valid(board, row, col, num, subgrid_rows, subgrid_cols):
    """Check if placing num at board[row][col] is valid."""
    n = len(board)  # Size of the board

    # Check the row
    if num in board[row]:
        return False

    # Check the column
    if num in [board[i][col] for i in range(n)]:
        return False

    # Check the subgrid
    start_row, start_col = (row // subgrid_rows) * subgrid_rows, (col // subgrid_cols) * subgrid_cols
    for i in range(start_row, start_row + subgrid_rows):
        for j in range(start_col, start_col + subgrid_cols):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board, subgrid_rows, subgrid_cols):
    """Recursive backtracking function to solve the Sudoku puzzle."""
    n = len(board)  # Size of the board
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:  # Empty cell
                for num in range(1, n + 1):  # Try numbers 1 to n
                    if is_valid(board, row, col, num, subgrid_rows, subgrid_cols):
                        board[row][col] = num
                        if solve_sudoku(board, subgrid_rows, subgrid_cols):
                            return True
                        board[row][col] = 0  # Backtrack
                return False  # No valid number found, backtrack
    return True

def get_sudoku_input(n):
    """Allow users to input a Sudoku puzzle."""
    print(f"Please enter a {n}x{n} Sudoku puzzle (use 0 for empty cells):")
    board = []
    for i in range(n):
        row = list(map(int, input(f"Enter row {i + 1}: ").split()))
        board.append(row)
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
    print("Welcome to the Sudoku Solver!")
    grid_size = int(input("Enter the Sudoku grid size (4, 6, 9): "))

    # Determine subgrid dimensions based on grid size
    if grid_size == 4:
        subgrid_rows, subgrid_cols = 2, 2
    elif grid_size == 6:
        subgrid_rows, subgrid_cols = 3, 2
    elif grid_size == 9:
        subgrid_rows, subgrid_cols = 3, 3
    else:
        print("Invalid grid size. Only 4x4, 6x6, and 9x9 are supported.")
        exit()

    choice = input("Do you want to input your own puzzle? (yes/no): ").strip().lower()
    
    if choice == 'yes':
        puzzle = get_sudoku_input(grid_size)
    else:
        puzzle = select_puzzle(grid_size)

    print("Original Puzzle:")
    print_board(puzzle)

    # Solve using Backtracking Algorithm
    print("Solving with Backtracking Algorithm...")
    puzzle_copy = [row[:] for row in puzzle]  # Copy the puzzle to avoid modifying the original
    if solve_sudoku(puzzle_copy, subgrid_rows, subgrid_cols):
        print("Solved Puzzle:")
        print_board(puzzle_copy)
    else:
        print("No solution exists using Backtracking Algorithm.")