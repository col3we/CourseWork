import datetime as dt
import json
import logging
import os
import re
from typing import Any, Hashable

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "services.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def investment_bank(month: str, transactions: list[dict[Hashable, Any]], limit: int) -> float:
    """Принимает на вход месяц в виде %Y-%m, список транзакций и лимит по которому будут округляться переводы
    То есть если число 1536 и лимит=50 то округляется до 1550 и в копилку ложится 14
    Выводит сумму которую вы могли заработать"""
    logger.info("Переводим строку с месяцем в дату в формате datetime")
    date = dt.datetime.strptime(month, "%Y-%m")
    summ = 0
    logger.info("Проходимся по списку в котором год и месяц совпадает и проводим округление")
    for i in transactions:
        trn_date = dt.datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if trn_date.year == date.year and trn_date.month == date.month:
            if i["Сумма операции"] % limit != 0:
                num = i["Сумма операции"] // limit
                inv_sum = i["Сумма операции"] - num * limit
                summ += inv_sum

    return round(summ, 2)


def description_filter(transactions: list[dict[Hashable, Any]], word: str) -> str:
    """Принимает на вход список транзакций
    и слово по которому надо фильтровать описание и категорию транзакций
    и выводит отфитрованный список"""
    logger.info(f"Делаем патерн слова {word}")
    pattern = re.compile(word, re.IGNORECASE)
    logger.info("Проходимся по списку и оставляем только нужные описания и транзакции")
    my_list = [
        transaction
        for transaction in transactions
        if pattern.search(str(transaction.get("Категория"))) or pattern.search(str(transaction.get("Описание")))
    ]

    return json.dumps(my_list, ensure_ascii=False)
