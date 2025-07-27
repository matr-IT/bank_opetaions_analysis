import logging


# Инициируем логгер для модуля reports
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/Users/rybin/PycharmProjects/bank_operations_analysis/logs/reports.log",
    filemode="w",
)
views_log = logging.getLogger(__name__)
