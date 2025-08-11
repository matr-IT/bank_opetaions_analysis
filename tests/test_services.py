import pytest
from unittest.mock import patch

from src.services import process_bank_search


@pytest.fixture
def mock_operations():
    return [
        {"Описание": "Покупка в магазине Ашан", "Категория": "Супермаркет"},
        {"Описание": "Оплата интернета", "Категория": "Связь"},
        {"Описание": "Перевод другу", "Категория": "Перевод"},
        {"Описание": "АШАН онлайн", "Категория": "Интернет-магазины"},
        {"Описание": "Такси Яндекс", "Категория": "Транспорт"},
    ]


@patch("builtins.open")
@patch("json.load")
@patch("pandas.read_excel")
def test_process_bank_search_match_description(mock_read_excel, mock_json_load, mock_open, mock_operations):

    mock_read_excel.return_value.to_dict.return_value = mock_operations

    result = process_bank_search("такси")

    assert len(result) == 237
    assert result[0]["Описание"] == "Яндекс Такси"


@patch("builtins.open")
@patch("json.load")
@patch("pandas.read_excel")
def test_process_bank_search_match_category(mock_read_excel, mock_json_load, mock_open, mock_operations):
    mock_read_excel.return_value.to_dict.return_value = mock_operations

    result = process_bank_search("связь")

    assert len(result) == 224
    assert result[0]["Категория"] == "Связь"


@patch("builtins.open")
@patch("json.load")
@patch("pandas.read_excel")
def test_process_bank_search_case_insensitive(mock_read_excel, mock_json_load, mock_open, mock_operations):
    mock_read_excel.return_value.to_dict.return_value = mock_operations

    result1 = process_bank_search("ашан")
    result2 = process_bank_search("АШАН")
    result3 = process_bank_search("аШаН")

    assert len(result1) == 1
    assert len(result2) == 1
    assert len(result3) == 1


@patch("builtins.open")
@patch("json.load")
@patch("pandas.read_excel")
def test_process_bank_search_match_both_fields(mock_read_excel, mock_json_load, mock_open, mock_operations):
    modified_ops = mock_operations + [{"Описание": "Ашан доставка", "Категория": "Ашан"}]
    mock_read_excel.return_value.to_dict.return_value = modified_ops

    result = process_bank_search("ашан")

    assert len(result) == 1
    assert all(("ашан" in item["Описание"].lower() or "ашан" in item["Категория"].lower()) for item in result)


@patch("builtins.open")
@patch("json.load")
@patch("pandas.read_excel")
def test_process_bank_search_no_results(mock_read_excel, mock_json_load, mock_open, mock_operations):
    mock_read_excel.return_value.to_dict.return_value = mock_operations

    result = process_bank_search("несуществующий запрос")

    assert result == "Транзакции не обнаружены"
