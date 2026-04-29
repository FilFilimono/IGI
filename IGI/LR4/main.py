"""
Description: Global Execution Module for Lab 1 (Tasks 1-6).
Lab Number: 1
Title: Advanced Python OOP and Data Processing
Version: 3.0
Author: Filipp Filimonov
Date: 2026-04-16
"""

import sys
import os

# Импортируем инструменты из utils
from utils import execute_with_retry, get_valid_integer, ZeroDenominatorError

# Импорты для Заданий 1 и 2
from task1 import RationalNumber, CsvSerializer, PickleSerializer, check_duplicates, find_maximum
from task2 import TextAnalyzer, save_and_archive_results

# Импорты для Задания 3
from task3 import ArcSinCalculator, plot_functions

# Импорты для Задания 4
from task4 import RegularHexagon

# Импорты для Заданий 5 и 6
import task5
import task6

@execute_with_retry
def run_task1():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 1: Рациональные числа")
    print("="*40)
    
    # Генерация тестовых данных
    data = {f"num_{i}": RationalNumber(i, i+1) for i in range(1, 6)}
    
    csv_ser = CsvSerializer()
    csv_ser.save(data, 'data.csv')
    print("Данные сохранены в data.csv")

    rationals = list(data.values())
    print(f"Максимальное число из списка: {find_maximum(rationals)}")
    
    num = get_valid_integer("Введите числитель для теста: ")
    den = get_valid_integer("Введите знаменатель для теста: ")
    try:
        user_val = RationalNumber(num, den)
        print(f"Объект создан: {user_val}")
    except ZeroDenominatorError as e:
        print(f"Ошибка: {e}")

@execute_with_retry
def run_task2():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 2: Регулярные выражения")
    print("="*40)
    analyzer = TextAnalyzer('text_input.txt')
    results = {**analyzer.analyze_general(), **analyzer.analyze_variant()}
    save_and_archive_results(results, 'results.txt', 'archive.zip')
    print("Анализ завершен. Результаты в archive.zip")

@execute_with_retry
def run_task3():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 3: Ряд Тейлора arcsin(x)")
    print("="*40)
    x = 0.5
    calc = ArcSinCalculator(x)
    print("Таблица результатов:")
    print("-" * 51)
    calc.print_table_row()
    print("-" * 51)
    plot_functions()

@execute_with_retry
def run_task4():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 4: Геометрия (Шестиугольник)")
    print("="*40)
    side = float(input("Введите сторону 'a': "))
    color = input("Введите цвет (напр. green): ")
    text = input("Введите текст подписи: ")
    
    hex_fig = RegularHexagon(side, color)
    print(hex_fig.get_info())
    hex_fig.draw(text)

@execute_with_retry
def run_task5():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 5: Исследование NumPy")
    print("="*40)
    task5.main()

@execute_with_retry
def run_task6():
    print("\n" + "="*40)
    print("ЗАДАНИЕ 6: Pandas и Titanic Dataset")
    print("="*40)
    
    # Демонстрация основ (Series/DataFrame)
    task6.demonstrate_part_a()
    
    # Работа с реальным датасетом
    dataset_name = 'train.csv'
    if os.path.exists(dataset_name):
        task6.analyze_titanic_data(dataset_name)
    else:
        print(f"\n[!] Файл {dataset_name} не найден в текущей папке.")
        print("Пожалуйста, скачайте Titanic train.csv с Kaggle.")

def main_menu():
    """Главное меню управления лабораторной работой."""
    menu_options = {
        '1': ("Задание 1: Рациональные числа", run_task1),
        '2': ("Задание 2: Анализ текста", run_task2),
        '3': ("Задание 3: Ряды и Math", run_task3),
        '4': ("Задание 4: ООП и Фигуры", run_task4),
        '5': ("Задание 5: Матрицы NumPy", run_task5),
        '6': ("Задание 6: Анализ Titanic (Pandas)", run_task6),
        '0': ("Выход", sys.exit)
    }

    while True:
        print("\n" + "#"*50)
        print("   ЦЕНТРАЛЬНОЕ УПРАВЛЕНИЕ ЛАБОРАТОРНОЙ РАБОТОЙ")
        print("#"*50)
        for key, (desc, _) in menu_options.items():
            print(f"{key}. {desc}")
            
        choice = input("\nВыберите действие: ").strip()
        
        if choice in menu_options:
            if choice == '0':
                print("Программа завершена.")
                menu_options[choice][1]()
            else:
                menu_options[choice][1]() # Запуск выбранной функции
        else:
            print("Ошибка: Неверный пункт меню.")

if __name__ == "__main__":
    main_menu()