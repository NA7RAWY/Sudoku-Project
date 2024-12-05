import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from time import time
from backtracking_solver import solve_sudoku as solve_with_backtracking, is_valid
from genetic_solver import genetic_algorithm


class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.grid_size = 9  # Default grid size
        self.entries = []

        # Welcome message
        self.welcome_label = tk.Label(self.root, text="Welcome to Sudoku Solver", font=("Arial", 16), fg="blue")
        self.welcome_label.pack(pady=10)

        # Create a frame for the Sudoku grid
        self.grid_frame = tk.Frame(self.root, bg="black", relief="solid", bd=2)
        self.grid_frame.pack(pady=10)

        # Create a frame for controls
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Algorithm selection dropdown
        self.algorithm_var = tk.StringVar(value="Backtracking")
        self.algorithm_label = tk.Label(self.control_frame, text="Select Algorithm:")
        self.algorithm_label.grid(row=0, column=0, padx=5)
        self.algorithm_menu = ttk.OptionMenu(
            self.control_frame, self.algorithm_var, "Backtracking", "Backtracking", "Genetic Algorithm"
        )
        self.algorithm_menu.grid(row=0, column=1, padx=5)

        # Define button dimensions
        button_width = 20
        button_height = 2

        # Solve button
        self.solve_button = tk.Button(
            self.control_frame, text="Solve", command=self.solve_puzzle,
            bg="green", fg="white", width=button_width, height=button_height
        )
        self.solve_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Clear button
        self.clear_button = tk.Button(
            self.control_frame, text="Clear", command=self.clear_puzzle,
            bg="red", fg="white", width=button_width, height=button_height
        )
        self.clear_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Load puzzle button
        self.puzzle_button = tk.Button(
            self.control_frame, text="Load Puzzle", command=self.load_puzzle,
            bg="blue", fg="white", width=button_width, height=button_height
        )
        self.puzzle_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Make your puzzle button
        self.make_your_puzzle_button = tk.Button(
            self.control_frame, text="Make Your Puzzle", command=self.make_your_puzzle,
            bg="purple", fg="white", width=button_width, height=button_height
        )
        self.make_your_puzzle_button.grid(row=4, column=0, columnspan=2, pady=5)

        # Return to Main Menu button
        self.main_menu_button = tk.Button(
            self.control_frame, text="Return to Main Menu", command=self.return_to_main_menu,
            bg="gray", fg="white", width=button_width, height=button_height
        )
        self.main_menu_button.grid(row=5, column=0, columnspan=2, pady=5)

        # Performance metrics label
        self.metrics_label = tk.Label(self.root, text="Performance Metrics: ", font=("Arial", 12), fg="black")
        self.metrics_label.pack(pady=10)


    def create_grid(self, grid_size):
        """Create a Sudoku grid dynamically based on the grid size."""
        # Clear the existing grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid_size = grid_size
        self.entries = []

        subgrid_rows, subgrid_cols = self.get_subgrid_dimensions(grid_size)

        for row in range(self.grid_size):
            row_entries = []
            for col in range(self.grid_size):
                entry = tk.Entry(self.grid_frame, width=2, font=("Arial", 16), justify="center", bg="white")
                top_border = 2 if row % subgrid_rows == 0 and row != 0 else 1
                left_border = 2 if col % subgrid_cols == 0 and col != 0 else 1
                entry.grid(row=row, column=col, padx=(left_border, 1), pady=(top_border, 1))
                entry.bind("<KeyRelease>", self.validate_input)
                row_entries.append(entry)
            self.entries.append(row_entries)


    def validate_input(self, event):
        """Validate the input in the Sudoku grid."""
        widget = event.widget
        value = widget.get().strip().upper()  # Convert to uppercase for consistency

        # Get valid inputs based on the current grid size
        valid_inputs = self.get_valid_inputs(self.grid_size)

        # Check if the entered value is valid
        if value not in valid_inputs and value != "":
            widget.delete(0, tk.END)  # Clear invalid input
            widget.insert(0, "")  # Set the input to an empty string
            messagebox.showwarning(
                "Invalid Input", f"Please enter a valid input. Valid range: {', '.join(valid_inputs)}"
            )
        else:
            # Additional check for numbers above the grid size
            try:
                number = int(value)
                if number > self.grid_size:
                    widget.delete(0, tk.END)  # Clear invalid input
                    widget.insert(0, "")  # Set the input to an empty string
                    messagebox.showwarning(
                        "Invalid Input", f"Please enter a number less than or equal to {self.grid_size}."
                    )
            except ValueError:
                # Handle non-numeric input (already handled by the previous check)
                pass



    def get_puzzle(self):
        """Retrieve the current puzzle from the grid."""
        puzzle = []
        for row_entries in self.entries:
            row = []
            for entry in row_entries:
                value = entry.get().strip()
                row.append(int(value) if value.isdigit() else 0)
            puzzle.append(row)
        return puzzle

    def display_solution(self, solution):
        """Display the solved puzzle on the grid."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.entries[row][col].delete(0, tk.END)
                value = solution[row][col]
                # Display hexadecimal characters for 16x16 grid
                if isinstance(value, int) and value > 9:
                    value = chr(value + 55)  # Convert 10-15 to A-G
                self.entries[row][col].insert(0, str(value))


    def clear_puzzle(self):
        """Clear the Sudoku grid."""
        for row_entries in self.entries:
            for entry in row_entries:
                entry.delete(0, tk.END)
        self.metrics_label.config(text="Performance Metrics: ")

    def load_puzzle(self):
        """Prompt the user to select the grid size and load a predefined puzzle."""
        grid_size = simpledialog.askinteger(
            "Choose Grid Size", "Enter grid size (4, 6, 9, or 16):", parent=self.root, minvalue=4, maxvalue=16
        )

        if grid_size not in [4, 6, 9, 16]:
            messagebox.showerror("Error", "Invalid grid size selected.")
            return

        self.create_grid(grid_size)
        predefined_puzzle = self.get_predefined_puzzle(grid_size)

        for row in range(grid_size):
            for col in range(grid_size):
                value = predefined_puzzle[row][col]
                if value != 0:
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(value))

    def get_predefined_puzzle(self, grid_size):
        """Return a predefined puzzle based on the grid size."""
        if grid_size == 4:
            return [
                [1, 0, 0, 4],
                [0, 0, 3, 0],
                [0, 1, 0, 0],
                [3, 0, 0, 2]
            ]
        elif grid_size == 6:
            return [
                [2, 0, 0, 1, 5, 0],
                [0, 0, 0, 0, 0, 0],
                [4, 5, 2, 3, 1, 0],
                [1, 0, 0, 0, 0, 4],
                [6, 0, 0, 0, 0, 0],
                [3, 0, 0, 6, 0, 5]
            ]

        elif grid_size == 9:
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
        elif grid_size == 16:
            return [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]


    def make_your_puzzle(self):
        """Allow the user to create their puzzle after selecting grid size."""
        grid_size = simpledialog.askinteger(
            "Choose Grid Size", "Enter grid size (4, 6, 9, or 16):", parent=self.root, minvalue=4, maxvalue=16
        )
        if grid_size not in [4, 6, 9, 16]:
            messagebox.showerror("Error", "Invalid grid size selected.")
            return

        # Create the grid for the selected size
        self.create_grid(grid_size)

        # Set up input validation dynamically for the selected grid size
        for row_entries in self.entries:
            for entry in row_entries:
                entry.bind("<KeyRelease>", self.validate_input)

        # Provide instructions to the user
        valid_inputs = self.get_valid_inputs(grid_size)

    def get_valid_inputs(self, grid_size):
        """Return valid inputs for the grid size."""
        if grid_size == 4:
            return [str(i) for i in range(1, 5)]  # 1 to 4
        elif grid_size == 6:
            return [str(i) for i in range(1, 7)]  # 1 to 6
        elif grid_size == 9:
            return [str(i) for i in range(1, 10)]  # 1 to 9
        elif grid_size == 16:
            # 1-9 and A-F for 16x16 grids
            return [str(i) for i in range(1, 10)] + [chr(i) for i in range(ord('A'), ord('G') + 1)]
        else:
            return []  # Empty for unsupported sizes

    def return_to_main_menu(self):
        """Return to the main menu."""
        self.root.quit()

        os.execv(sys.executable, ['python'] + sys.argv)

    def validate_input(self, event):
        """Validate the input in the Sudoku grid."""
        widget = event.widget
        value = widget.get().strip()
        if not (value.isdigit() and 1 <= int(value) <= 9):
            widget.delete(0, tk.END)

    def solve_puzzle(self):
        """Solve the puzzle using the selected algorithm."""
        puzzle = self.get_puzzle()
        algorithm = self.algorithm_var.get()
        subgrid_rows, subgrid_cols = self.get_subgrid_dimensions(self.grid_size)

        start_time = time()  # Start timing

        if algorithm == "Backtracking":
            puzzle_copy = [row[:] for row in puzzle]
            subgrid_rows, subgrid_cols = self.get_subgrid_dimensions(self.grid_size)
            if solve_with_backtracking(puzzle_copy, subgrid_rows, subgrid_cols):
                self.display_solution(puzzle_copy)
                time_taken = time() - start_time
                self.metrics_label.config(
                    text=f"Performance Metrics: Algorithm: Backtracking | Time Taken: {time_taken:.4f} seconds"
                )
            else:
                messagebox.showerror("Error", "No solution exists for the given puzzle.")
        elif algorithm == "Genetic Algorithm":
            solution, generations = genetic_algorithm(puzzle, n=self.grid_size)
            time_taken = time() - start_time
            if solution:
                self.display_solution(solution)
                self.metrics_label.config(
                    text=f"Performance Metrics: Algorithm: Genetic Algorithm | Generations: {generations} | Time Taken: {time_taken:.4f} seconds"
                )
            else:
                messagebox.showerror("Error", "No solution found using Genetic Algorithm.")    


    def get_subgrid_dimensions(self, grid_size):
        """Calculate subgrid dimensions for the given grid size."""
        if grid_size == 4:
            return 2, 2  # 4×4 grid has 2×2 sub-grids
        elif grid_size == 6:
            return 2, 3  # 6×6 grid has 2×3 sub-grids
        elif grid_size == 9:
            return 3, 3  # 9×9 grid has 3×3 sub-grids
        elif grid_size == 16:
            return 4, 4  # 16×16 grid has 4×4 sub-grids
        else:
            raise ValueError("Unsupported grid size.")



# Main function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()

sys.setrecursionlimit(10000)