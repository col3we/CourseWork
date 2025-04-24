import datetime
import json
import logging
import os
from math import isnan

from src.external_api import get_currency, get_stocks
from src.utils import XLSX_file_read

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "views.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_sheet(date: str):
    """Главная функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающую JSON-ответ
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    user_set_path = os.path.join(base_dir, "..", "user_settings.json")
    logger.info("Открываем и читаем файл")
    with open(user_set_path, encoding="utf-8") as f:
        data = json.load(f)
    file = XLSX_file_read()
    answer = {"greeting": "", "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}

    logger.info("Переводим строку с датой в формат datetime и по времени выводим сообщение с приветствием")
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    message = ""
    if 0 <= date.hour < 6:
        message = "Доброе утро"
    elif 6 <= date.hour < 12:
        message = "Добрый день"
    elif 12 <= date.hour < 18:
        message = "Добрый вечер"
    elif 18 <= date.hour < 24:
        message = "Доброй ночи"

    logger.info("Фильтруем операции за период с начала месяца по указанную дату")
    start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    filtered_transactions = []
    for i in file:
        payment_date = datetime.datetime.strptime(i["Дата платежа"], "%d.%m.%Y")
        if start_date <= payment_date <= date:
            filtered_transactions.append(i)

    logger.info(f"Отфильтрованные даты платежей: {[elem['Дата платежа'] for elem in filtered_transactions]}")

    logger.info("Вызываем функцию чтобы получить банковские карты")
    cards = get_cards(filtered_transactions)

    logger.info("Сортируем список по сумме операций и получаем самые большие транзакции")
    top_transactions = get_top_transactions(filtered_transactions)

    logger.info("Получаем курс валют пользователя с помощью API")
    currency_rates = get_currency(data)

    logger.info("Получаем стоимость акций пользователя с помощью API")
    stock_prices = get_stocks(data)

    logger.info("Записываем ответы в вывод")
    answer["greeting"] = message
    answer["cards"] = cards
    answer["top_transactions"] = top_transactions
    answer["currency_rates"] = currency_rates
    answer["stock_prices"] = stock_prices

    return json.dumps(answer, ensure_ascii=False)


def get_top_transactions(data):
    """Принимает на вход список транзакций, сортируем его по убыванию суммы и выводим 5 самых больших транзакций"""
    top_transactions = []
    sorted_file = sorted(data, key=lambda x: x.get("Сумма операции с округлением", 0), reverse=True)
    for i in range(min(5, len(sorted_file))):
        top_transactions.append(
            {
                "date": sorted_file[i]["Дата операции"][:10],
                "amount": sorted_file[i]["Сумма операции с округлением"],
                "category": sorted_file[i]["Категория"],
                "description": sorted_file[i]["Описание"],
            }
        )
    return top_transactions


def get_cards(file):
    numbers = []
    cards = []
    for i in file:
        card_num = i["Номер карты"][1:]
        if card_num not in numbers:
            numbers.append(card_num)

    for num in numbers:
        cards.append({"last_digits": num, "total_spent": 0, "cashback": 0})

    for i in file:
        card_num = i["Номер карты"][1:]
        for j in cards:
            if card_num == j["last_digits"]:
                if i["Сумма операции"] < 0:
                    j["total_spent"] += i["Сумма операции с округлением"]
                if not isnan(i["Кэшбэк"]):
                    j["cashback"] += i["Кэшбэк"]

    for i in cards:
        i["total_spent"] = round(i["total_spent"], 2)
        i["cashback"] = round(i["cashback"], 2)

    return cards
