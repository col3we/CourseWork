import datetime
import json

import pandas as pd

from src import services, views
from src.utils import XLSX_file_read
from src.reports import spending_by_category


def main():
    date = "2022-08-15 11:22:14"
    datetime_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Получаем основной JSON-ответ с данными по картам, транзакциям, курсам и акциям
    main_data_json = views.main_sheet(date)
    main_data = json.loads(main_data_json)

    print(main_data)
    print(main_data["greeting"])
    print("Информация по картам:")

    for card in main_data["cards"]:
        print(
            f"""         [Карта:{card['last_digits']}
         Потраченная сумма за этот месяц: {card['total_spent']}
         Заработанный кешбэк:{card['cashback']}]\n"""
        )

    print("Самые большие транзакции в этом месяце:")
    for tr in main_data["top_transactions"]:
        print(
            f"""         [Дата:{tr['date']}
         Сумма транзакции: {tr['amount']}"""
        )
        if pd.isna(tr["category"]):
            print("         Категория отсутствует")
        else:
            print(f"         Категория:{tr['category']}")
        if pd.isna(tr["description"]):
            print("         Описание отсутствует]\n")
        else:
            print(f"         Описание:{tr['description']}]\n")

    print("Текущий курс валют:")
    for rate in main_data["currency_rates"]:
        print(f"{rate['currency']} = {rate['rate']}")

    print("Текущая стоимость акций:")
    for stock in main_data["stock_prices"]:
        print(f"{stock['stock']} = {stock['price']}")

    transactions_df = XLSX_file_read()
    category = "Продукты"
    date_str = datetime_date.strftime("%Y-%m-%d")

    category_spending = spending_by_category(transactions_df, category, date_str)
    print(f"Расходы по категории '{category}' за последние 3 месяца от {date_str}: {category_spending[category]}")

    print("Введите лимит для инвесткопилки")
    limit = int(input())
    year_month = f"{datetime_date.year}-{datetime_date.month:02d}"
    bank = services.investment_bank(year_month, transactions_df, limit)
    print(f"Сумму которую вы могли заработать за этот месяц - {bank}")


if __name__ == "__main__":
    main()
