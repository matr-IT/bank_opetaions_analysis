import json
import datetime
from calendar import month

import pandas as pd
from dateutil.relativedelta import relativedelta

from views import load_transactions

operations = load_transactions("/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx")


def spending_by_category(transactions,  category, date= None):
    if not date:
        date = datetime.datetime.now()
    date = pd.to_datetime(date)
    first_day_of_period = date + relativedelta(months=-3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    filtered = transactions[transactions["Дата операции"] >= first_day_of_period]
    filtered = filtered[filtered["Дата операции"] <= date]
    filtered = filtered.to_dict(orient="records")

    result = []
    for transaction in filtered:
        if category == transaction["Категория"]:
            result.append(transaction)

    return result

print((spending_by_category(operations, "Супермаркеты", "31.12.2021 16:42:04")))



