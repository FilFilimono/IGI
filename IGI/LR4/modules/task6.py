import pandas as pd
import os
from utils.mixins import InfoMixin

"""
Purpose: Pandas library exploration and statistical analysis
Lab: #6 (Task 6) - SuperMarket Dataset
Version: 1.0
Author: [Ваше Ф.И.О.]
Date: 2026-04-29
"""

class PandasAnalyzer(InfoMixin):
   
    def __init__(self, filepath=os.path.join("data", "SuperMarketAnalysis.csv")):
        self.filepath = filepath
        self.df = self._load_data()

    def _load_data(self):
   
        if os.path.exists(self.filepath):
            print(f"[*] Данные успешно загружены из {self.filepath}...\n")
            return pd.read_csv(self.filepath)
        else:
            raise FileNotFoundError(f"Файл датасета {self.filepath} не найден в текущей директории.")

    def demonstrate_series_and_basic_ops(self):
   
        print("\n--- ЗАДАНИЕ А: Pandas Basics ---")
        
   
        sample_series = pd.Series([100, 200, 300], index=['A', 'B', 'C'], name="Sample")
        print("1. Созданная структура Series:")
   
        print(sample_series) 
        

        print("\n2. Доступ к элементам Series (.loc и .iloc):")
        print(f"   Использование .loc['B']: {sample_series.loc['B']}")
        print(f"   Использование .iloc[2]: {sample_series.iloc[2]}")
        

        print("\n3. Создание DataFrame из категориальной Series с порядком ('Product line'):")
        

        unique_lines = self.df['Product line'].unique().tolist()
        cat_type = pd.CategoricalDtype(categories=unique_lines, ordered=True)
        

        cat_series = self.df['Product line'].astype(cat_type)
        

        codes = cat_series.cat.codes
        
        
        cat_df = pd.DataFrame({
            'Product Line Name': cat_series,
            'Category Code': codes
        })
        
        print(cat_df.head(10).to_string())

    def perform_statistical_analysis(self):
        
        print("\n--- ЗАДАНИЕ Б: Статистический анализ ---")
        
        print("\n1. Информация о датафрейме:")
        
        import io
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        print(buffer.getvalue())

        print("\n2. Статистическое задание:")
        
        total_col = 'Sales' if 'Sales' in self.df.columns else 'Total'
        
       
        self.df['Hour'] = pd.to_datetime(self.df['Time']).dt.hour
        
    
        hourly_revenue = self.df.groupby('Hour')[total_col].sum()
        
        max_profit_hour = hourly_revenue.idxmax() 
        min_profit_hour = hourly_revenue.idxmin() 
        
    
        mean_receipt_max = self.df[self.df['Hour'] == max_profit_hour][total_col].mean()
        mean_receipt_min = self.df[self.df['Hour'] == min_profit_hour][total_col].mean()
        
    
        ratio = mean_receipt_max / mean_receipt_min if mean_receipt_min > 0 else 0
        
        print(f"Самый прибыльный час: {max_profit_hour}:00 (Суммарная выручка: {hourly_revenue[max_profit_hour]:.2f})")
        print(f"Самый непродаваемый час: {min_profit_hour}:00 (Суммарная выручка: {hourly_revenue[min_profit_hour]:.2f})")
        
        print(f"\nСредний чек в прибыльный час ({max_profit_hour}:00): {mean_receipt_max:.2f}")
        print(f"Средний чек в непродаваемый час ({min_profit_hour}:00): {mean_receipt_min:.2f}")
        
    
        print(f"\nОтвет: Средний доход с чека (Total/Sales) в самый прибыльный час работы "
              f"больше, чем в самый непродаваемый час, в {ratio:.2f} раз(а).")

def run_task_6():
    
    print("\n--- Task 6: Pandas Data Analysis ---")
    try:
        analyzer = PandasAnalyzer()
        analyzer.log_action("Started Pandas analysis for SuperMarket dataset")
        analyzer.demonstrate_series_and_basic_ops()
        analyzer.perform_statistical_analysis()
    except FileNotFoundError as e:
        print(f"Ошибка файлов: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка в Pandas: {e}")
        
