import csv
import pickle
import os
from utils.mixins import InfoMixin
from utils.validators import get_int_input

"""
Purpose: Handling rational numbers with serialization (CSV/Pickle)
Lab: #X (Task 1)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class BaseNumber:
    """Base class for numerical entities."""
    def __init__(self, description="Numerical data"):
        self.description = description

class Rational(BaseNumber, InfoMixin):
    """
    Class representing a rational number [numerator, denominator].
    Demonstrates: super(), properties, getters/setters, magic methods.
    """
    # Static attribute (Requirement 4)
    instance_count = 0

    def __init__(self, numerator, denominator):
        super().__init__("Rational Number")
        self._numerator = numerator
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self._denominator = denominator
        Rational.instance_count += 1
        self.log_action("Created rational number")

    # Property with Getter and Setter (Requirement 4)
    @property
    def numerator(self):
        """Getter for numerator."""
        return self._numerator

    @numerator.setter
    def numerator(self, value):
        self._numerator = value

    @property
    def denominator(self):
        """Getter for denominator."""
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        if value == 0:
            raise ValueError("Denominator cannot be zero.")
        self._denominator = value

    def to_float(self):
        """Calculates the float value of the rational number."""
        return self._numerator / self._denominator

    # Magic methods for polymorphism and comparison (Requirement 4)
    def __eq__(self, other):
        if not isinstance(other, Rational):
            return False
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __gt__(self, other):
        return self.to_float() > other.to_float()

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

class RationalManager:
    """Handles collections of Rational numbers and Serialization."""
    
    @staticmethod
    def save_to_csv(data_dict, filename):
        """Serializes dictionary to CSV."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for k, v in data_dict.items():
                    writer.writerow([k, v.numerator, v.denominator])
            print(f"Successfully saved to {filename}")
        except Exception as e:
            print(f"CSV Save Error: {e}")

    @staticmethod
    def save_to_pickle(data_dict, filename):
        """Serializes dictionary using Pickle."""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data_dict, f)
            print(f"Successfully saved to {filename}")
        except Exception as e:
            print(f"Pickle Save Error: {e}")

def run_task_1():
    """Main function for Task 1 execution."""
    print("\n--- Task 1: Rational Numbers ---")
    
    numbers_dict = {}
    print("Enter 10 rational numbers:")
    for i in range(1, 11):
        print(f"Number {i}:")
        num = get_int_input("  Numerator: ")
        den = get_int_input("  Denominator (not 0): ")
        while den == 0:
            print("Error: Denominator cannot be 0.")
            den = get_int_input("  Denominator: ")
        numbers_dict[f"n{i}"] = Rational(num, den)

    # a) Check for equals
    found_equal = False
    vals = list(numbers_dict.values())
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if vals[i] == vals[j]:
                found_equal = True
                break
    
    print(f"\nEqual numbers found: {'Yes' if found_equal else 'No'}")

    # b) Find maximum
    max_rational = max(vals, key=lambda x: x.to_float())
    print(f"Maximum rational number: {max_rational}")

    # Serialization
    RationalManager.save_to_csv(numbers_dict, "data.csv")
    RationalManager.save_to_pickle(numbers_dict, "data.pickle")

    # User input search
    print("\nSearch for a number:")
    s_num = get_int_input("Enter numerator: ")
    s_den = get_int_input("Enter denominator: ")
    search_obj = Rational(s_num, s_den)
    print(f"Info about entered: {search_obj.get_class_info()} -> {search_obj}")
    
    
#Здесь реализована работа с рациональными числами, сериализация (CSV, Pickle) и ООП.