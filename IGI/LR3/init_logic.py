"""
Purpose: Sequence initialization using yield.
Lab: 3
Version: 1.0
Author: Filipp Filimonov
"""

def user_input_generator(size):
    """Yields numbers entered by user."""
    for i in range(size):
        while True:
            try:
                yield float(input(f"Enter element {i+1}: "))
                break
            except ValueError:
                print("Invalid input.")

def random_generator(size):
    """Yields random numbers using a simple math logic."""
    import random
    for _ in range(size):
        yield round(random.uniform(-0.9, 0.9), 4)