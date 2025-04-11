import datetime
import json

import pandas as pd

from src import services, views
from src.utils import XLSX_file_read


def main():
    date = "2022-08-15 11:22:14"
    datetime_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    main_data = views.main_sheet(date)
    main_data = json.loads(main_data)
    print(main_data)
    print(main_data["greeting"])
    print("Информация по картам:")

    for i in range(len(main_data["cards"])):
        print(
            f"""         [Карта:{main_data['cards'][i]['last_digits']}
         Потраченная сумма за этот месяц: {main_data['cards'][i]['total_spent']}
         Заработанный кешбэк:{main_data['cards'][i]['cashback']}]\n"""
        )

    print("Самые большие транзакции в этом месяце:")
    for i in range(len(main_data["top_transactions"])):
        print(
            f"""         [Дата:{main_data['top_transactions'][i]['date']}
         Сумма транзакции: {main_data['top_transactions'][i]['amount']}"""
        )
        if pd.isna(main_data["top_transactions"][i]["category"]):
            print("         Категория отсутствует")
        else:
            print(f"         Категория:{main_data['top_transactions'][i]['category']}")
        if pd.isna(main_data["top_transactions"][i]["description"]):
            print("         Описание отсутствует]\n")
        else:
            print(f"         Описание:{main_data['top_transactions'][i]['description']}]\n")

    print("Текущий курс валют:")
    for i in range(len(main_data["currency_rates"])):
        print(f"{main_data['currency_rates'][i]['currency']} = {main_data['currency_rates'][i]['rate']}")

    print("Текущая стоимость акций:")
    for i in range(len(main_data["stock_prices"])):
        print(f"{main_data['stock_prices'][i]['stock']} = {main_data['stock_prices'][i]['price']}")

    print("Введите лимит для инвесткопилки")
    limit = int(input())
    year_month = f"{datetime_date.year}-{datetime_date.month}"
    bank = services.investment_bank(year_month, XLSX_file_read(), limit)
    print(f"Сумму которую вы могли заработать за этот месяц - {bank}")


main()
