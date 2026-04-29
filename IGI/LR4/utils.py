"""
Description: Utility functions, custom exceptions, and logic decorators.
Lab Number: 1
Title: Advanced Python OOP and Data Processing
Version: 2.0
Author: Filipp Filimonov
Date: 2026-04-16
"""

class ZeroDenominatorError(Exception):
    """Custom exception for zero denominator in rational numbers."""
    pass

class LoggerMixin:
    """Mixin for logging object creation and actions."""
    def log(self, message: str) -> None:
        print(f"[LOG]: {message}")

def get_valid_integer(prompt: str) -> int:
    """Validation for integer inputs."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a valid integer.")

def execute_with_retry(func):
    """Decorator to allow task re-execution without exiting the program."""
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
            choice = input("\nRepeat this task? (y/n): ").strip().lower()
            if choice != 'y':
                break
    return wrapper