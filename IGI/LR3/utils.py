"""
Purpose: Simple utilities and a decorator with scope examples.
Lab: 3
Version: 1.0
Author: Filipp Filimonov
"""


APP_NAME = "Lab3_App"

def simple_decorator(func):
    """Decorator to show scopes."""
    prefix = "[LOG]" 

    def wrapper(*args, **kwargs):
        status = "Started"
        print(f"{prefix} {APP_NAME}: {func.__name__} is {status}")
        return func(*args, **kwargs)
    return wrapper

def get_int(prompt):
    """Safe integer input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Enter an integer.")

def get_float(prompt):
    """Safe float input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Enter a number.")