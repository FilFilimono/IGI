"""
Purpose: Input validation functions
Lab: #X (General Utils)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

def get_int_input(prompt, min_val=None, max_val=None):
   
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Error: Value must be at most {max_val}.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid integer.")

def get_non_empty_string(prompt):
    
    while True:
        data = input(prompt).strip()
        if data:
            return data
        print("Error: Input cannot be empty.")
        


