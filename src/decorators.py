import datetime
import json
import os
from functools import wraps


def report_writer(filename=None):
    """Декоратор для записи результатов отчетов в файл"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename:
                file_name = filename
            else:
                func_name = func.__name__
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{func_name}_{timestamp}.json"

            os.makedirs("reports", exist_ok=True)
            file_path = os.path.join("reports", file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                if isinstance(result, (dict, list)):
                    json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(result))

            print(f"Отчет сохранен в файл: {file_path}")
            return result

        return wrapper

    return decorator
