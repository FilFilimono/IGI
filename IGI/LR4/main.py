"""
Purpose: Main entry point for the application, connecting all modules.
Lab: Final Compilation
Version: 1.0
Author: [Your Name]
Date: 2026-04-29
"""

import sys
import os
from utils.validators import get_int_input
from modules.task1 import run_task_1
from modules.task2 import run_task_2
from modules.task3 import run_task_3
from modules.task4 import run_task_4
from modules.task5 import run_task_5
from modules.task6 import run_task_6
"""
Purpose: Main entry point for the application, connecting all modules.
Lab: Final Compilation
Version: 1.1
Author: [Ваше Ф.И.О.]
Date: 2026-04-29
"""

import sys
import os
from utils.validators import get_int_input
from modules.task1 import run_task_1
from modules.task2 import run_task_2
from modules.task3 import run_task_3
from modules.task4 import run_task_4
from modules.task5 import run_task_5
from modules.task6 import run_task_6

def main_menu():
    os.makedirs('data', exist_ok=True)
    
    while True:
        print("\n" + "="*40)
        print("      PYTHON LAB WORK - MAIN MENU      ")
        print("="*40)
        print("1. Task 1: Rational Numbers (Serialization & OOP)")
        print("2. Task 2: Text Analysis (RegEx & ZipFile)")
        print("3. Task 3: Arcsin Taylor Series (Matplotlib & Stats)")
        print("4. Task 4: Geometric Figures (OOP, Inheritance)")
        print("5. Task 5: Matrix Operations (NumPy)")
        print("6. Task 6: Data Analysis (Pandas)")
        print("0. Exit")
        print("="*40)

        choice = get_int_input("Select an option (0-6): ", min_val=0, max_val=6)

        try:
            if choice == 1:
                run_task_1()
            elif choice == 2:
                run_task_2()
            elif choice == 3:
                run_task_3()
            elif choice == 4:
                run_task_4()
            elif choice == 5:
                run_task_5()
            elif choice == 6:
                run_task_6()
            elif choice == 0:
                print("Exiting program. Goodbye!")
                sys.exit(0)
        except Exception as e:
            print(f"\n[GLOBAL ERROR] An unexpected error occurred: {e}")
            print("Returning to main menu...")

if __name__ == "__main__":
    main_menu()