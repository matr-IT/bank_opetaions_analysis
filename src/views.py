import json
from importlib.metadata import pass_none
from typing import List, Dict, Any

import pandas as pd
import datetime



def greeting():
    """Приветствие исходя из текущего времени"""
    time = datetime.datetime.now()
    hour = time.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

greet = greeting()

def load_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и выдает DataFrame"""
    try:
        df = pd.read_excel(file_path)
        return df
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)


def get_card_info(date_time: str) -> list[
    dict[str, str] | dict[str, list[dict[str, float | int | Any]]] | dict[str, str] | dict[str, str] | dict[str, str]]:
    """Функция отображает данные по картам: номер, сумму трат по карте и полученный кэшбэк"""
    date_time_pd = pd.to_datetime(date_time)
    operations = load_transactions('/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx')
    operations["Дата операции"] = pd.to_datetime(operations["Дата операции"])
    first_day_of_month = date_time_pd.replace(day=1)
    filtered = operations[operations["Дата операции"] >= first_day_of_month]
    filtered = filtered[filtered["Дата операции"] <= date_time_pd]

    card_data = []
    for card in filtered['Номер карты'].dropna().unique():
        card_transactions = filtered[filtered['Номер карты'] == card]
        total_spent = card_transactions["Сумма операции"].sum() * -1
        card_data.append({
            "last_digits": card[-4:],
            "total_spent": round(float(total_spent), 2),
            "cashback": round(float(total_spent * 0.01))
        })

    filtered = filtered.sort_values(by='Сумма операции', ascending=True)
    filtered = filtered.head(5)
    required_columns = ['Дата операции', 'Сумма операции', 'Категория', 'Описание']
    top_transactions = filtered[required_columns].to_dict(orient="records")

    currency_rates = []


    return [{"greeting": greet},
            {"cards": card_data},
            {"top_transactions": top_transactions},
            {"currency_rates": "pass"},
            {"stock_prices": "pass"}]

print(get_card_info('2021-01-29 22:49:17'))