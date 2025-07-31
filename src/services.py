import json
import re


from views import load_transactions


def process_bank_search(search=None) -> json:
    """Filters operations by keyword from their descriptions"""

    operations = load_transactions(
        "/Users/rybin/PycharmProjects/bank_operations_analysis/data/operations.xlsx"
    ).to_dict(orient="records")

    if not search:
        return operations

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []

    for i in operations:
        description = i["Описание"]
        if pattern.search(description):
            result.append(i)

    if result:
        return result
    else:
        return "Транзакции не обнаружены"


print(process_bank_search())
