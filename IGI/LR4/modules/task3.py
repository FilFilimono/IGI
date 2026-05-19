import math
import os
import statistics
import matplotlib.pyplot as plt
from utils.mixins import InfoMixin
from utils.exceptions import MathDomainError
from utils.validators import get_int_input

"""
Purpose: Taylor series calculation for arcsin(x) and statistical analysis
Lab: #3 (Task 3)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class ArcsinSeries(InfoMixin):
    def __init__(self, x, epsilon):
        if not (-1 < x < 1):
            raise MathDomainError("For arcsin(x) Taylor series, |x| must be < 1.")
        self.x = x
        self.epsilon = epsilon
        self.sequence_values = []
        self.math_value = math.asin(x)
        self.iterations = 0

    def calculate_series(self):
        n = 0
        current_sum = 0
        term = self.x 

        print(f"\n{'x':<10} | {'n':<5} | {'F(x)':<15} | {'Math F(x)':<15} | {'eps':<15}")
        print("-" * 70)

        while abs(term) >= self.epsilon and n < 100: # Limit to 100 to avoid infinite loops
            current_sum += term
            self.sequence_values.append(current_sum)
            
            print(f"{self.x:<10.5f} | {n:<5} | {current_sum:<15.10f} | {self.math_value:<15.10f} | {abs(term):<15.10f}")
            
            n += 1
            numerator = math.factorial(2 * n)
            denominator = (4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1)
            term = (numerator / denominator) * (self.x ** (2 * n + 1))
            
        self.iterations = n
        return current_sum

    def get_statistics(self):
        if not self.sequence_values:
            return {}
        
        try:
            mode_val = statistics.mode(self.sequence_values)
        except statistics.StatisticsError:
            mode_val = "No unique mode"

        stats = {
            "mean": statistics.mean(self.sequence_values),
            "median": statistics.median(self.sequence_values),
            "mode": mode_val,
        }
        
        if len(self.sequence_values) > 1:
            stats["variance"] = statistics.variance(self.sequence_values)
            stats["stdev"] = statistics.stdev(self.sequence_values)
        else:
            stats["variance"] = 0
            stats["stdev"] = 0
            
        return stats

    def plot_graphs(self):
        if not self.sequence_values:
            self.calculate_series()

        n_values = list(range(self.iterations))
        math_values = [self.math_value] * self.iterations

        plt.figure(figsize=(10, 6))
        plt.plot(n_values, self.sequence_values, color='blue', label='Taylor Series F(x)', marker='o')
        plt.plot(n_values, math_values, color='red', linestyle='--', label='math.asin(x)')
        
        plt.title(f"Approximation of arcsin({self.x})")
        plt.xlabel("Number of terms (n)")
        plt.ylabel("Function Value F(x)")
        
        plt.legend()

        
        plt.text(0, self.math_value + 0.05, f"Target value: {self.math_value:.4f}", color='red')
        plt.grid(True)
        filename = os.path.join("data", "arcsin_plot.png")
        plt.savefig(filename)
        print(f"\nPlot saved successfully to {filename}")
        plt.show()

def run_task_3():
    print("\n--- Task 3: Arcsin Taylor Series ---")
    try:
        x_val = float(input("Enter x (-1 < x < 1): "))
        eps_val = float(input("Enter epsilon (e.g., 0.0001): "))
        
        series = ArcsinSeries(x_val, eps_val)
        series.log_action("Calculated Series")
        series.calculate_series()
        
        stats = series.get_statistics()
        print("\nStatistical Parameters:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key.capitalize()}: {value:.6f}")
            else:
                print(f"  {key.capitalize()}: {value}")
                
        series.plot_graphs()
    except ValueError:
        print("Error: Invalid numeric input.")
    except MathDomainError as e:
        print(f"Domain Error: {e.message}")
        
