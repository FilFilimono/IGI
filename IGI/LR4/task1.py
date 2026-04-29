"""
Description: Task 1 - Rational numbers processing and serialization (CSV/Pickle).
Lab Number: 1
Author: Filipp Filimonov
Date: 2026-04-16
"""
import csv, pickle, os
from abc import ABC, abstractmethod
from utils import LoggerMixin, ZeroDenominatorError

class BaseNumber(ABC):
    total_created = 0
    def __init__(self):
        BaseNumber.total_created += 1
    @abstractmethod
    def get_value(self): pass

class RationalNumber(BaseNumber, LoggerMixin):
    def __init__(self, numerator: int, denominator: int):
        super().__init__()
        self._numerator = numerator
        self.denominator = denominator # triggering setter
        self.log(f"Rational {self} created.")

    @property
    def numerator(self): return self._numerator
    @numerator.setter
    def numerator(self, v): self._numerator = v

    @property
    def denominator(self): return self._denominator
    @denominator.setter
    def denominator(self, v):
        if v == 0: raise ZeroDenominatorError("Denominator is zero!")
        self._denominator = v

    def get_value(self): return self.numerator / self.denominator
    def __str__(self): return f"{self.numerator}/{self.denominator}"
    def __eq__(self, other):
        return self.numerator * other.denominator == other.numerator * self.denominator
    def __lt__(self, other):
        return self.numerator * other.denominator < other.numerator * self.denominator

class CsvSerializer:
    def save(self, data, filename):
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for k, v in data.items(): writer.writerow([k, v.numerator, v.denominator])
    def load(self, filename):
        if not os.path.exists(filename): return {}
        res = {}
        with open(filename, 'r') as f:
            for r in csv.reader(f): res[r[0]] = RationalNumber(int(r[1]), int(r[2]))
        return res

class PickleSerializer:
    def save(self, data, filename):
        with open(filename, 'wb') as f: pickle.dump(data, f)
    def load(self, filename):
        if not os.path.exists(filename): return {}
        with open(filename, 'rb') as f: return pickle.load(f)

def check_duplicates(lst): return len(lst) != len(set(str(x) for x in lst))
def find_maximum(lst): return max(lst) if lst else None