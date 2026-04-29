"""
Description: Task 3 - Taylor series for arcsin(x) and plotting.
Lab Number: 1
Author: Filipp Filimonov
Date: 2026-04-16
"""
import math, statistics, matplotlib.pyplot as plt

class ArcSinCalculator:
    def __init__(self, x, eps=1e-5):
        self.x, self.eps = x, eps
        self.terms = []
        self.val = self._calc()

    def _calc(self):
        res, n = 0.0, 0
        while True:
            term = (math.factorial(2*n) / (4**n * (math.factorial(n)**2) * (2*n+1))) * (self.x**(2*n+1))
            self.terms.append(term)
            res += term
            if abs(term) < self.eps: break
            n += 1
        self.n = n
        return res

    def get_statistics(self):
        return {
            "Mean": statistics.mean(self.terms),
            "Median": statistics.median(self.terms),
            "StdDev": statistics.stdev(self.terms) if len(self.terms) > 1 else 0
        }

    def print_table_row(self):
        print(f"| {self.x:^8.2f} | {self.n:^5} | {self.val:^10.5f} | {math.asin(self.x):^10.5f} | {self.eps:^8} |")

def plot_functions():
    x = [i/100 for i in range(-90, 91)]
    y_approx = [ArcSinCalculator(xv).val for xv in x]
    plt.plot(x, y_approx, 'b--', label='Taylor Series')
    plt.plot(x, [math.asin(xv) for xv in x], 'r', alpha=0.5, label='Math.asin')
    plt.legend(); plt.grid(True); plt.show()