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
