"""
Purpose: Task 1 - Taylor series for arcsin(x).
"""
import math
from utils import simple_decorator

@simple_decorator
def calculate_arcsin(x, eps):
    """Taylor series calculation for arcsin."""
    if not -1 < x < 1:
        return None
    
    n = 0
    res = 0
    term = x
    
    while n < 500:
        res += term
        if abs(term) < eps:
            break
        # Recurrence relation for arcsin
        term *= ((2*n + 1)**2 * x**2) / ((2*n + 2) * (2*n + 3))
        n += 1
    return res, n, math.asin(x)