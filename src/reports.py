import datetime
import logging
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta

from views import load_transactions

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "reports.log"

LOG_DIR.mkdir(exist_ok=True, parents=True)

logging.basicConfig(filemode="w")
logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

operations = load_transactions("/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx")


def spending_by_category(transactions, category, date=None):
    """Функция сортирует траты по категории"""
    logger.info("Проверяем наличие аргумента 'дата'")
    if not date:
        date = datetime.datetime.now()
    date = pd.to_datetime(date)
    logger.info("Определяем первый день отчетного периода")
    first_day_of_period = date + relativedelta(months=-3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    filtered = transactions[transactions["Дата операции"] >= first_day_of_period]
    filtered = filtered[filtered["Дата операции"] <= date]
    filtered = filtered.to_dict(orient="records")

    result = []
    logger.info("Определяем транзакции, подходящие под фильтр")
    for transaction in filtered:
        if category == transaction["Категория"]:
            result.append(transaction)
    if result:
        return result
    else:
        return "Транзакции в данной категории не обнаружены"
