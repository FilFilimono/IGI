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
    def __init__(self, description="Numerical data"):
        self.description = description

class Rational(BaseNumber, InfoMixin):
    instance_count = 0

    def __init__(self, numerator, denominator):
        super().__init__("Rational Number")
        self._numerator = numerator
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self._denominator = denominator
        Rational.instance_count += 1
        self.log_action("Created rational number")

    @property
    def numerator(self):
        return self._numerator

    @numerator.setter
    def numerator(self, value):
        self._numerator = value

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, value):
        if value == 0:
            raise ValueError("Denominator cannot be zero.")
        self._denominator = value

    def to_float(self):
        return self._numerator / self._denominator

    def __eq__(self, other):
        if not isinstance(other, Rational):
            return False
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __gt__(self, other):
        return self.to_float() > other.to_float()

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

class RationalManager:
    
    @staticmethod
    def save_to_csv(data_dict, filename):
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
        try:
            with open(filename, 'wb') as f:
                pickle.dump(data_dict, f)
            print(f"Successfully saved to {filename}")
        except Exception as e:
            print(f"Pickle Save Error: {e}")
            
    @staticmethod
    def load_from_csv(filename):
        try:
            data_dict = {}
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:  
                        key = row[0]
                        numerator = int(row[1])
                        denominator = int(row[2])
            print(f"Successfully loaded from {filename}")
            return data_dict
        except Exception as e:
            print(f"CSV Load Error: {e}")
            return None

    @staticmethod
    def load_from_pickle(filename):
        try:
            with open(filename, 'rb') as f:
                data_dict = pickle.load(f)
            print(f"Successfully loaded from {filename}")
            return data_dict
        except Exception as e:
            print(f"Pickle Load Error: {e}")
            return None

def run_task_1():
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

    found_equal = False
    vals = list(numbers_dict.values())
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if vals[i] == vals[j]:
                found_equal = True
                break
    
    print(f"\nEqual numbers found: {'Yes' if found_equal else 'No'}")

    max_rational = max(vals, key=lambda x: x.to_float())
    print(f"Maximum rational number: {max_rational}")

    RationalManager.save_to_csv(numbers_dict, os.path.join("data", "data.csv"))
    RationalManager.save_to_pickle(numbers_dict, os.path.join("data", "data.pickle"))

    print("\nSearch for a number:")
    s_num = get_int_input("Enter numerator: ")
    s_den = get_int_input("Enter denominator: ")
    search_obj = Rational(s_num, s_den)
    print(f"Info about entered: {search_obj.get_class_info()} -> {search_obj}")
    
    
