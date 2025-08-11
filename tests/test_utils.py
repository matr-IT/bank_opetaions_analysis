from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import greeting, load_transactions


@pytest.mark.parametrize(
    "hour, expected",
    [
        (4, "Доброй ночи"),
        (5, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (23, "Добрый вечер"),
        (0, "Доброй ночи"),
    ],
)
def test_greeting(hour, expected):
    """
    Проверяем корректность приветствия для разных часов
    """
    mock_time = datetime(2024, 1, 1, hour, 0, 0)

    with patch("src.utils.datetime") as mock_datetime, patch("src.utils.logger", MagicMock()):
        mock_datetime.now.return_value = mock_time

        result = greeting()

        assert result == expected


@pytest.fixture
def mock_excel_file(tmp_path):
    """Фикстура для создания временного Excel-файла"""
    file_path = tmp_path / "test.xlsx"

    df = pd.DataFrame({"id": [1, 2, 3], "amount": [100, 200, 300]})

    df.to_excel(file_path, index=False)
    return file_path


def test_successful_load(mock_excel_file, caplog):
    """Тест успешной загрузки файла"""
    result = load_transactions(str(mock_excel_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ["id", "amount"]


@patch("src.utils.pd.read_excel")
def test_file_not_found_error(mock_read_excel, caplog):
    """Тест обработки ошибки отсутствия файла"""
    mock_read_excel.side_effect = FileNotFoundError("Файл не найден")

    result = load_transactions("non_existent_file.xlsx")

    assert result is None


@patch("src.utils.pd.read_excel")
def test_value_error(mock_read_excel, caplog):
    """Тест обработки ошибки невалидного файла"""
    mock_read_excel.side_effect = ValueError("Неправильный формат")

    result = load_transactions("invalid_file.xlsx")

    assert result is None
