import pandas as pd
from pandas.core.frame import DataFrame 

columns_to_exclude = ["Вычеты Вычеты всего", "Доход", 'Вычеты', "Налог-Удержано всего", 'Unnamed: 6']  


def accept_file(file: str) -> DataFrame:
    """Принимает документ .xlsx, исключение стобцов, подготовка для вычислений"""
    df = pd.read_excel(file)
    df = df.dropna(subset=["Сотрудник"]) 
    df = df.drop(columns=columns_to_exclude, errors="ignore") 
    return df


