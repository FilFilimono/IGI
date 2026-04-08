"""
Purpose: Task 2 - Find max until 1.
"""
from utils import simple_decorator, get_int

@simple_decorator
def find_max_sequence():
    """Finds maximum number. Stops at 1."""
    m = None
    print("Enter numbers (1 to stop):")
    while True:
        val = get_int("> ")
        if val == 1: break
        if m is None or val > m: m = val
    return m