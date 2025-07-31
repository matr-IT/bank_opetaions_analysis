import re
import logging

# Инициируем логгер для модуля services
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/Users/rybin/PycharmProjects/bank_operations_analysis/logs/services.log",
    filemode="w",
)
views_log = logging.getLogger(__name__)
