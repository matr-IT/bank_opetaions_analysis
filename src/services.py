import json
import logging
import re
from pathlib import Path

from views import load_transactions

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "services.log"

LOG_DIR.mkdir(exist_ok=True, parents=True)

logging.basicConfig(filemode="w")
logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def process_bank_search(search=None) -> json:
    """Фильтрует операции по ключевым словам из описания операции или категории"""
    logger.info("Загружаем список операций")
    operations = load_transactions(
        "/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx"
    ).to_dict(orient="records")
    logger.info("Проверяем наличие ключевых слов для поиска")
    if not search:
        return operations

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    logger.info("Проверяем наличие ключевых слов в описании или категории операции")
    for i in operations:
        description = i["Описание"]
        category = i["Категория"]
        if pattern.search(description) or pattern.search(str(category)):
            result.append(i)

    if result:
        return result
    else:
        return "Транзакции не обнаружены"


# print(process_bank_search("РЖД"))
