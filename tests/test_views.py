import json
import os
from unittest.mock import mock_open, patch

import pandas as pd
import pytest
import requests

from src.views import get_card_info


@pytest.fixture
def mock_transactions_data():
    return pd.DataFrame(
        {
            "Дата операции": ["2023-10-05", "2023-10-12", "2023-10-18", "2023-09-28", "2023-10-25", "2023-10-03"],
            "Номер карты": [
                "123456****3456",
                "123456****3456",
                "987654****4321",
                "123456****3456",
                "987654****4321",
                "123456****3456",
            ],
            "Сумма операции": [-1000, -2500, -500, -300, -1500, -200],
            "Категория": ["Food", "Tech", "Transport", "Food", "Tech", "Transport"],
            "Описание": ["Supermarket", "Laptop", "Taxi", "Cafe", "Phone", "Bus"],
        }
    )


@pytest.fixture
def mock_user_settings():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


@patch("requests.get")
@patch("os.getenv")
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_get_card_info_success(
    mock_read_excel, mock_file_open, mock_os_getenv, mock_requests_get, mock_transactions_data, mock_user_settings
):
    mock_read_excel.return_value = mock_transactions_data
    mock_file_open.return_value.read.return_value = json.dumps(mock_user_settings)
    mock_os_getenv.side_effect = lambda x: "test_api_key" if "API_KEY" in x else None

    mock_currency_response = requests.Response()
    mock_currency_response.status_code = 200
    mock_currency_response.json = lambda: {"result": 75.0}

    mock_stock_response = requests.Response()
    mock_stock_response.status_code = 200
    mock_stock_response.json = lambda: {"Global Quote": {"08. previous close": "150.0"}}

    mock_requests_get.side_effect = [
        mock_currency_response,
        mock_currency_response,
        mock_stock_response,
        mock_stock_response,
    ]

    result = get_card_info("2023-10-20")

    assert isinstance(result, list)
    assert len(result) == 5

    assert result[0] == {"greeting": "Добрый вечер"}

    cards = result[1]["cards"]
    assert len(cards) == 2
    assert cards == [
        {"last_digits": "3456", "total_spent": 3700.0, "cashback": 37},
        {"last_digits": "4321", "total_spent": 500.0, "cashback": 5},
    ]

    top_transactions = result[2]["top_transactions"]
    assert len(top_transactions) == 4
    assert [t["Сумма операции"] for t in top_transactions] == [-2500, -1000, -500, -200]

    assert result[3]["currency_rates"] == [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 75.0}]

    assert result[4]["stock_prices"] == [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOGL", "price": 150.0}]


@patch("requests.get")
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_get_card_info_no_data(mock_read_excel, mock_file_open, mock_requests_get, mock_user_settings):
    mock_read_excel.return_value = pd.DataFrame(
        columns=["Дата операции", "Номер карты", "Сумма операции", "Категория", "Описание"]
    )
    mock_file_open.return_value.read.return_value = json.dumps(mock_user_settings)

    result = get_card_info("2023-11-01")

    assert result[1]["cards"] == []
    assert result[2]["top_transactions"] == []
    assert len(result[3]["currency_rates"]) == 2
    assert len(result[4]["stock_prices"]) == 2
