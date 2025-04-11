import datetime
import logging
import os
from datetime import timedelta
from functools import wraps
from typing import Optional

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "reports.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_file_write(filename: str = "report.txt"):
    """Декоратор для сохранения результата функции-отчета в указанный файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            report_dir = os.path.join(base_dir, "..", "reports")
            report_file_path = os.path.join(report_dir, filename)
            logger.info(
                f"Создаём и открываем файл по пути {report_file_path} и записываем результат функции {func.__name__} = {result}"
            )
            with open(report_file_path, "w", encoding="utf-8") as file:
                file.write(str(result))
            return result

        return wrapper

    return decorator


@report_file_write(filename="my_report.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> dict:
    """Принимает на вход список транзакций, категорию и дату в формате %Y-%m-%d
    и выводит отфильтрованный список с нужными категориями и с начала введённой даты до 3 месяцев вперёд"""
    logger.info("Проверяем дана ли дата и переводим её в нужный формат")
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")

    date_2 = date - timedelta(days=90)
    logger.info(f"Получаем что дата через 3 месяца от даты {date} равна {date_2}")
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", dayfirst=True)
    logger.info("Фильтруем список транзакций по дате и категории")
    filter_transactions = transactions[
        (category == transactions["Категория"])
        & (transactions["Дата платежа"] >= date_2)
        & (transactions["Дата платежа"] <= date)
    ]
    summ = 0
    for i in filter_transactions["Сумма операции"]:
        if i < 0:
            summ += i
    logger.info(f"Находим сумму трат за 3 месяца от даты {date} с нужной категорией")
    result = {category: round(summ, 2)}
    return result
