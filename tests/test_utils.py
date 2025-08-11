import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from utils import greeting


@pytest.mark.parametrize("hour, expected", [
    (4, "Доброй ночи"),
    (5, "Доброе утро"),
    (11, "Доброе утро"),
    (12, "Добрый день"),
    (17, "Добрый день"),
    (18, "Добрый вечер"),
    (23, "Добрый вечер"),
    (0, "Доброй ночи"),
])
def test_greeting(hour, expected):
    """
    Проверяем корректность приветствия для разных часов
    """
    mock_time = datetime(2024, 1, 1, hour, 0, 0)

    with patch("utils.datetime") as mock_datetime, \
            patch("utils.logger", MagicMock()):
        mock_datetime.now.return_value = mock_time

        result = greeting()

        assert result == expected

