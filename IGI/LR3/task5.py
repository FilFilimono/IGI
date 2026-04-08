"""
Purpose: Task 5 - List processing.
"""
from utils import simple_decorator

@simple_decorator
def process_list(lst):
    """Product of even indices and sum between zeros."""
    # 1. Product of even indices (0, 2, 4...)
    prod = 1.0
    for i in range(0, len(lst), 2):
        prod *= lst[i]
        
    # 2. Sum between zeros
    try:
        first = lst.index(0)
        last = len(lst) - 1 - lst[::-1].index(0)
        s_mid = sum(lst[first+1:last]) if first < last else 0
    except ValueError:
        s_mid = "No zeros"
        
    return prod, s_mid