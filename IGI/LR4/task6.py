"""
Description: Task 6 - Pandas EDA using the Titanic Dataset.
Lab Number: 1
Author: Filipp Filimonov
Date: 2026-04-16
"""

import pandas as pd
import os

# Функция для красивого вывода в консоль (имитация Jupyter)
try:
    from IPython.display import display
except ImportError:
    display = print

def demonstrate_part_a():
    """
    ЗАДАНИЕ А: Работа со структурами Series и DataFrame.
    """
    print("\n" + "="*40)
    print("ЗАДАНИЕ А: Структуры Series и DataFrame")
    print("="*40)

    # 1. Библиотека Pandas уже импортирована как pd

    # 2 & 3. Структура Series и её создание
    # Создадим Series из данных о выживаемости (условно)
    survival_data = [0, 1, 1, 0, 1]
    labels = ['Pass_1', 'Pass_2', 'Pass_3', 'Pass_4', 'Pass_5']
    survival_series = pd.Series(data=survival_data, index=labels, name="Survived")
    
    # 4. Функция display
    print("\n--- 4. Функция display (Series) ---")
    display(survival_series)

    # 5. Доступ к элементам Series (.loc и .iloc)
    print("\n--- 5. Доступ к элементам ---")
    print(f"Доступ через .loc['Pass_3'] (по метке): {survival_series.loc['Pass_3']}")
    print(f"Доступ через .iloc[2] (по позиции): {survival_series.iloc[2]}")

    # 6. Объект DataFrame. Создание вручную.
    print("\n--- 6. Создание DataFrame вручную ---")
    manual_df = pd.DataFrame({
        'Name': ['Braund', 'Cumings', 'Heikkinen'],
        'Age': [22, 38, 26],
        'Survived': [0, 1, 1]
    })
    display(manual_df)


def analyze_titanic_data(filepath: str):
    """
    ЗАДАНИЕ Б: Статистический анализ датасета Titanic.
    """
    print("\n" + "="*40)
    print("ЗАДАНИЕ Б: Анализ данных Titanic")
    print("="*40)

    # Загрузка данных
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл {filepath} не найден. Проверьте путь.")
        return

    df = pd.read_csv(filepath)

    # 1. Получение информации о датафрейме
    print("\n--- Информация о датафрейме (df.info) ---")
    df.info()

    print("\n--- Описательная статистика (df.describe) ---")
    display(df.describe())

    # 2. Статистический расчет по варианту
    # Показатель: Стоимость билета (Fare)
    # Параметр для условий (Max/Min): Возраст (Age)
    
    # Удаляем строки с пустым возрастом для корректности
    clean_df = df.dropna(subset=['Age', 'Fare'])

    max_age = clean_df['Age'].max()
    min_age = clean_df['Age'].min()

    # Средняя цена билета для самых старых и самых молодых
    mean_fare_oldest = clean_df[clean_df['Age'] == max_age]['Fare'].mean()
    mean_fare_youngest = clean_df[clean_df['Age'] == min_age]['Fare'].mean()

    print(f"\n--- Результаты расчетов ---")
    print(f"Максимальный возраст (самый старый): {max_age} лет")
    print(f"Минимальный возраст (самый молодой): {min_age} лет")
    print("-" * 30)
    print(f"Средняя стоимость билета (Max Age): {mean_fare_oldest:.2f}")
    print(f"Средняя стоимость билета (Min Age): {mean_fare_youngest:.2f}")

    if mean_fare_youngest > 0:
        ratio = mean_fare_oldest / mean_fare_youngest
        print(f"\nВЫВОД: Средняя цена билета самого старого пассажира в {ratio:.2f} раз(а)")
        print(f"отличается от средней цены самого молодого.")
    
    # Математическая формулировка для отчета:
    # $$Ratio = \frac{\mu(Fare)_{Age=max}}{\mu(Fare)_{Age=min}}$$