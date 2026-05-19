import math
import os
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from utils.exceptions import InvalidDimensionError

"""
Purpose: Geometric shapes modeling and plotting (OOP, ABC)
Lab: #4 (Task 4)
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

class GeometricFigure(ABC):
    
    @abstractmethod
    def area(self):
        pass

class FigureColor:
    def __init__(self, color_name):
        self._color = color_name

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

class RegularHexagon(GeometricFigure):

    _figure_name = "Regular Hexagon"

    def __init__(self, side_a, color_name):
        if side_a <= 0:
            raise InvalidDimensionError("Hexagon side must be greater than 0.")
        self.side_a = side_a
        self.color_obj = FigureColor(color_name)
        self.label_text = "Hexagon"

    @classmethod
    def get_name(cls):
        
        return cls._figure_name

    def area(self):
        
        return (3 * math.sqrt(3) / 2) * (self.side_a ** 2)

    def get_info(self):
        
        return "Shape: {name}, Side: {side}, Color: {color}, Area: {area:.2f}".format(
            name=self.get_name(),
            side=self.side_a,
            color=self.color_obj.color,
            area=self.area()
        )

    def draw(self):
        
        fig, ax = plt.subplots(figsize=(6, 6))
        
        
        hexagon = patches.RegularPolygon(
            (0.5, 0.5), 
            numVertices=6,
            radius=self.side_a * 0.1, 
            facecolor=self.color_obj.color,
            edgecolor='black'
        )
        ax.add_patch(hexagon)
        
        plt.text(0.5, 0.5, self.label_text, color='white', 
                 ha='center', va='center', weight='bold', 
                 bbox=dict(facecolor='black', alpha=0.5))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        plt.axis('off')
        
        filename = os.path.join("data", "hexagon_plot.png")
        plt.savefig(filename)
        print(f"\nFigure saved to {filename}")
        plt.show()

def run_task_4():
    print("\n--- Task 4: OOP & Geometric Figures ---")
    try:
        side = float(input("Enter hexagon side 'a' (e.g. 2): "))
        color = input("Enter figure color (e.g. 'blue', 'green', 'red'): ").strip()
        label = input("Enter text to put on the figure: ").strip()
        
        hexagon = RegularHexagon(side, color)
        if label:
            hexagon.label_text = label
            
        print("\nFigure Info:")
        print(hexagon.get_info())
        
        print("\nDrawing figure...")
        hexagon.draw()
        
    except ValueError:
        print("Error: Invalid numeric input.")
    except InvalidDimensionError as e:
        print(f"Dimension Error: {e.message}")
        
