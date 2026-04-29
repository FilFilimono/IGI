"""
Description: Task 4 - OOP Geometry: Regular Hexagon.
Lab Number: 1
Author: Filipp Filimonov
Date: 2026-04-16
"""
import math, matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    @abstractmethod
    def area(self): pass

class FigureColor:
    def __init__(self, c): self.color = c

class RegularHexagon(GeometricFigure):
    name = "Regular Hexagon"
    def __init__(self, side, color):
        self.side = side
        self.color_obj = FigureColor(color)

    def area(self):
        return (3 * math.sqrt(3) / 2) * (self.side ** 2)

    def get_info(self):
        return "{0} of color {1}, side {2}. Area: {3:.2f}".format(self.name, self.color_obj.color, self.side, self.area())

    def draw(self, label):
        fig, ax = plt.subplots()
        hex_patch = RegularPolygon((0.5, 0.5), 6, 0.4, facecolor=self.color_obj.color, edgecolor='black')
        ax.add_patch(hex_patch)
        plt.text(0.5, 0.5, label, ha='center', va='center')
        ax.set_aspect('equal'); plt.axis('off'); plt.show()