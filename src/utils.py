import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "utils.log"

LOG_DIR.mkdir(exist_ok=True, parents=True)

logging.basicConfig(filemode="w")
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def greeting():
    """Приветствие исходя из текущего времени"""
    logger.info("Определяем текущее время")
    time = datetime.now()
    logger.info("Определяем текущий час")
    hour = time.hour
    logger.info("Определяем вариант приветствия")
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def load_transactions(file_path: str) -> pd.DataFrame:
    """Читает Excel-файл и выдает DataFrame"""
    logger.info("Пробуем открыть файл")
    try:
        df = pd.read_excel(file_path)
        return df
    except ValueError as ex:
        logger.error(f"Возникла ошибка {ex}")
        print(ex)
    except FileNotFoundError as ex:
        logger.error(f"Возникла ошибка {ex}")
        print(ex)
