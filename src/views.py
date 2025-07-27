import json
from os import remove
from unicodedata import category

import pandas as pd
import datetime



def greeting():
    """Приветствие исходя из текущего времени"""
    time = datetime.datetime.now()
    hour = time.hour
    if 5 <= hour < 12:
        return json.dumps("Доброе утро")
    elif 12 <= hour < 18:
        return json.dumps("Добрый день")
    elif 18 <= hour < 24:
        return json.dumps("Добрый вечер")
    else:
        return json.dumps("Доброй ночи")


def load_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и выдает DataFrame"""
    try:
        df = pd.read_excel(file_path)
        return df
    except ValueError as ex:
        print(ex)
    except FileNotFoundError as ex:
        print(ex)


def get_card_info(date_time: str) -> str:
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

    # top_transactions = []
    # if len(top_transactions) <= 5:
    #     for amount in filtered["Сумма операции"]:
    #         top_transaction_amounts = filtered[filtered["Сумма операции"] == amount]
    #         date = top_transaction_amounts["Дата операции"]
    #         amount = top_transaction_amounts["Сумма операции"]
    #         cat = top_transaction_amounts["Категория"]
    #         description = top_transaction_amounts["Описание"]
    #         top_transactions.append({
    #             "date": date,
    #             "amount": float(amount),
    #             "category": str(cat),
    #             "description": str(description)
    #         })



    final_data = [card_data]


    return final_data

print(get_card_info('2021-01-29 22:49:17'))