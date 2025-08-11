import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch

from src.reports import spending_by_category


@pytest.fixture
def sample_transactions():
    return pd.DataFrame({
        "Дата операции": [
            "2023-10-05", "2023-09-10", "2023-08-15",
            "2023-07-20", "2023-01-01", "2023-11-01"
        ],
        "Категория": [
            "Еда", "Транспорт", "Еда",
            "Еда", "Развлечения", "Транспорт"
        ],
        "Сумма операции": [100, 200, 150, 300, 400, 250],
        "Описание": [
            "Продукты", "Такси", "Ресторан",
            "Супермаркет", "Кино", "Метро"
        ]
    })




# Тест на получение транзакций с указанием даты
def test_spending_by_category_specific_date(sample_transactions):
    test_date = "2023-09-30"

    result = spending_by_category(sample_transactions, "Еда", date=test_date)

    assert len(result) == 2
    assert all(t["Категория"] == "Еда" for t in result)
    dates = [t["Дата операции"] for t in result]

    assert "2023-08-15" in dates
    assert "2023-07-20" in dates
    assert "2023-10-05" not in dates  # За пределами периода


# Тест на отсутствие транзакций в категории
@patch("datetime.datetime")
def test_spending_by_category_no_transactions(mock_datetime, sample_transactions):
    mock_datetime.now.return_value = datetime(2023, 11, 15)
    mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

    result = spending_by_category(sample_transactions, "Несуществующая")

    assert result == "Транзакции в данной категории не обнаружены"


# Тест на граничные даты периода
def test_spending_by_category_edge_dates(sample_transactions):
    edge_date = "2023-08-15"

    result = spending_by_category(sample_transactions, "Еда", date=edge_date)

    assert len(result) == 2
    dates = [t["Дата операции"] for t in result]
    assert "2023-08-15" in dates
    assert "2023-07-20" in dates
    assert "2023-10-05" not in dates




    # Тест на пустые входные данные


def test_empty_transactions():
    empty_df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма операции", "Описание"])

    result = spending_by_category(empty_df, "Еда")

    assert result == "Транзакции в данной категории не обнаружены"


