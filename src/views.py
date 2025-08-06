import datetime
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from utils import greeting, load_transactions

load_dotenv()


greet = greeting()


def get_card_info(date_time: str):
    """Функция отображает данные по картам: номер, сумму трат по карте и полученный кэшбэк, также отображает топ транзакций. курс пользовательских валют и стоимость пользовательских акций"""
    date_time_pd = pd.to_datetime(date_time)
    operations = load_transactions("/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx")
    operations["Дата операции"] = pd.to_datetime(operations["Дата операции"])
    first_day_of_month = date_time_pd.replace(day=1)
    filtered = operations[operations["Дата операции"] >= first_day_of_month]
    filtered = filtered[filtered["Дата операции"] <= date_time_pd]

    card_data = []
    for card in filtered["Номер карты"].dropna().unique():
        card_transactions = filtered[filtered["Номер карты"] == card]
        total_spent = card_transactions["Сумма операции"].sum() * -1
        card_data.append(
            {
                "last_digits": card[-4:],
                "total_spent": round(float(total_spent), 2),
                "cashback": round(float(total_spent * 0.01)),
            }
        )

    filtered = filtered.sort_values(by="Сумма операции", ascending=True)
    filtered = filtered.head(5)
    required_columns = ["Дата операции", "Сумма операции", "Категория", "Описание"]
    top_transactions = filtered[required_columns].to_dict(orient="records")

    with open("/Users/rybin/PycharmProjects/bank_operations_analysis/user_settings.json") as f:
        data = json.load(f)
    currencies = data["user_currencies"]
    stocks = data["user_stocks"]
    currency_rates = []
    stock_prices = []
    for cur in currencies:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={cur}&amount={1}"
        headers = {"apikey": os.getenv("API_KEY_EXCHANGE")}
        response = requests.get(url, headers=headers)
        response = response.json()
        rate = float(response["result"])
        currency_rates.append({"currency": cur, "rate": rate})

    for st in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={st}&apikey=API_KEY_STOCK_PRICES"
        headers = {"apikey": os.getenv("API_KEY_STOCK_PRICES")}
        response = requests.get(url, headers=headers)
        response = response.json()
        price = float(response["Global Quote"]["08. previous close"])
        stock_prices.append({"stock": st, "price": price})

    return json.dumps([
        {"greeting": greet},
        {"cards": card_data},
        {"top_transactions": top_transactions},
        {"currency_rates": currency_rates},
        {"stock_prices": stock_prices},
    ])


# print(get_card_info("31-12-2021 16:42:04"))
