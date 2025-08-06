import json
import re

from views import load_transactions


def process_bank_search(search=None) -> json:
    """Фильтрует операции по ключевым словам из описания операции или категории"""

    operations = load_transactions(
        "/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx"
    ).to_dict(orient="records")

    if not search:
        return operations

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []

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