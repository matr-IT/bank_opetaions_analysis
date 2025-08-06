from datetime import datetime

import pandas as pd


def greeting():
    """Приветствие исходя из текущего времени"""
    time = datetime.now()
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и выдает DataFrame"""
    try:
        df = pd.read_excel(file_path)
        return df
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)
