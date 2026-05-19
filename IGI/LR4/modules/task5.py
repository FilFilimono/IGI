import numpy as np
from utils.validators import get_int_input
from utils.exceptions import InvalidDimensionError

"""
Purpose: NumPy matrix manipulations and statistical operations
Lab: #5 (Task 5)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class MatrixAnalyzer:

    def __init__(self, n, m):
        if n < 1 or m < 1:
            raise InvalidDimensionError("Matrix dimensions must be at least 1x1.")
        
        self.matrix = np.random.randint(1, 100, size=(n, m))
        print("Original Matrix:")
        print(self.matrix)

    def demonstrate_numpy_features(self):
        
        print("\n--- NumPy Features Showcase ---")
        
        zeros_arr = np.zeros((2, 2))
        print("Zeros array:\n", zeros_arr)
        
        
        print("Slice of first 2 rows and columns:\n", self.matrix[:2, :2])
        
        
        print(f"Mean of matrix: {np.mean(self.matrix):.2f}")
        print(f"Variance of matrix: {np.var(self.matrix):.2f}")
        print(f"Standard Dev of matrix: {np.std(self.matrix):.2f}")
        
        if self.matrix.shape[0] > 1:
            print("Correlation matrix of first 2 rows:\n", np.corrcoef(self.matrix[0], self.matrix[1]))

    def execute_individual_task(self):
        
        print("\n--- Individual Task Execution ---")
        
        
        min_val = np.min(self.matrix)
        
        min_indices = np.unravel_index(np.argmin(self.matrix, axis=None), self.matrix.shape)
        min_row_idx = min_indices[0]
        
        print(f"First minimum element is {min_val} at row index {min_row_idx}")
        
        
        first_row = self.matrix[0]
        
        modified_matrix = np.insert(self.matrix, min_row_idx + 1, first_row, axis=0)
        
        print("\nModified Matrix:")
        print(modified_matrix)
        
        
        row_to_analyze = modified_matrix[0]
        
        
        std_median = np.median(row_to_analyze)
        
        
        sorted_row = np.sort(row_to_analyze)
        m = len(sorted_row)
        if m % 2 == 1:
            custom_median = sorted_row[m // 2]
        else:
            custom_median = (sorted_row[m // 2 - 1] + sorted_row[m // 2]) / 2.0
            
        print(f"\nFirst row: {row_to_analyze}")
        print(f"Median (NumPy function): {std_median}")
        print(f"Median (Custom formula): {custom_median}")

def run_task_5():
    
    print("\n--- Task 5: NumPy Matrix Analysis ---")
    try:
        n = get_int_input("Enter number of rows (n): ", min_val=1)
        m = get_int_input("Enter number of columns (m): ", min_val=1)
        
        analyzer = MatrixAnalyzer(n, m)
        analyzer.demonstrate_numpy_features()
        analyzer.execute_individual_task()
        
    except InvalidDimensionError as e:
        print(f"Dimension Error: {e.message}")
        