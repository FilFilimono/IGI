"""
Description: Task 5 - In-depth research of NumPy library capabilities.
Lab Number: 1
Title: Advanced Python OOP and Data Processing
Version: 3.0
Author: Filipp Filimonov
Date: 2026-04-16
"""

import numpy as np

def calculate_manual_median(arr):
    """
    Вычисление медианы через программирование формулы.
    Для нечетного n: средний элемент.
    Для четного n: среднее арифметическое двух средних элементов.
    """
    sorted_arr = sorted(arr)
    n = len(sorted_arr)
    index = n // 2
    if n % 2 == 0:
        return (sorted_arr[index - 1] + sorted_arr[index]) / 2
    else:
        return sorted_arr[index]

def main():
    print("--- Part A: Исследование возможностей NumPy ---")
    
    # 1. Создание массива через array() и использование .values (в pandas) 
    # Примечание: в чистом NumPy используется атрибут .data или просто сам массив
    simple_list = [1, 2, 3, 4, 5]
    arr_from_list = np.array(simple_list)
    print(f"1. Массив из списка: {arr_from_list}")

    # 2. Функции создания массивов заданного вида
    zeros = np.zeros((2, 2))
    ones = np.ones((2, 2))
    identity = np.eye(3) # Единичная матрица
    print(f"2. Единичная матрица:\n{identity}")

    # 3. Индексирование и срезы
    # Сформируем матрицу A[n, m] случайных чисел (Задание)
    n, m = 4, 5
    A = np.random.randint(0, 100, size=(n, m))
    print(f"\nИсходная матрица A[{n}x{m}]:\n{A}")
    print(f"Срез (первые 2 строки, колонки 1-3):\n{A[:2, 1:4]}")

    # 4. Универсальные (поэлементные) функции
    print(f"Квадрат каждого элемента (np.square):\n{np.square(A[:2, :2])}")

    print("\n--- Part B: Математические и статистические операции ---")
    print(f"1. Среднее значение (mean): {np.mean(A):.2f}")
    print(f"2. Медиана всей матрицы (median): {np.median(A)}")
    print(f"3. Коэффициенты корреляции (corrcoef):\n{np.corrcoef(A)}")
    print(f"4. Дисперсия (var): {np.var(A):.2f}")
    print(f"5. Стандартное отклонение (std): {np.std(A):.2f}")

    print("\n--- Индивидуальное задание ---")
    
    # Находим первый встреченный минимальный элемент
    min_val = np.min(A)
    # np.where возвращает (array_rows, array_cols)
    rows, cols = np.where(A == min_val)
    first_min_row_idx = rows[0]
    
    print(f"Минимум {min_val} найден в строке с индексом: {first_min_row_idx}")

    # Вставляем первую строку ПОСЛЕ строки с минимальным элементом
    first_row = A[0].copy()
    A_modified = np.insert(A, first_min_row_idx + 1, first_row, axis=0)
    print(f"Матрица после вставки первой строки:\n{A_modified}")

    # Вычисление медианы первой строки двумя способами
    target_row = A[0]
    med_np = np.median(target_row)
    med_manual = calculate_manual_median(target_row)

    print(f"\nМедиана первой строки {target_row}:")
    print(f"- Способ 1 (Standard NumPy): {med_np}")
    print(f"- Способ 2 (Manual Formula): {med_manual}")

if __name__ == "__main__":
    main()