import json
from unittest.mock import patch

from src.views import get_cards, get_top_transactions, main_sheet

sample_data = [
    {
        "Дата операции": "01.01.2025 12:00:00",
        "Дата платежа": "01.01.2025",
        "Сумма операции с округлением": 1000.0,
        "Сумма операции": -1000.0,
        "Категория": "Рестораны",
        "Описание": "Starbucks",
        "Номер карты": "*1234",
        "Кэшбэк": 10.0,
    },
    {
        "Дата операции": "02.01.2025 13:00:00",
        "Дата платежа": "02.01.2025",
        "Сумма операции с округлением": 2000.0,
        "Сумма операции": -2000.0,
        "Категория": "Магазины",
        "Описание": "Auchan",
        "Номер карты": "*1234",
        "Кэшбэк": 20.0,
    },
]


def test_get_top_transactions():
    result = get_top_transactions(sample_data)
    assert len(result) == 2
    assert result[0]["amount"] == 2000.0
    assert result[1]["amount"] == 1000.0


def test_get_cards():
    result = get_cards(sample_data)
    assert len(result) == 1
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == 3000.0
    assert result[0]["cashback"] == 30.0


@patch("src.views.XLSX_file_read", return_value=sample_data)
@patch("src.views.get_currency", return_value=[{"USD": 90.1}, {"EUR": 98.7}])
@patch(
    "src.views.get_stocks",
    return_value=[{"AAPL": 153.4}, {"AMZN": 3421.5}, {"GOOGL": 2720.2}, {"MSFT": 299.1}, {"TSLA": 721.3}],
)
@patch("builtins.open")
@patch("json.load", return_value={"currency": ["USD"], "stocks": ["AAPL"]})
def test_main_sheet(mock_json, mock_open, mock_stocks, mock_currency, mock_xlsx):
    date = "2025-01-03 11:00:00"
    result = main_sheet(date)
    result_dict = json.loads(result)
    assert result_dict["greeting"] == "Добрый день"

    date = "2025-01-03 19:00:00"
    result = main_sheet(date)
    result_dict = json.loads(result)
    assert result_dict["greeting"] == "Доброй ночи"

    date = "2025-01-03 5:00:00"
    result = main_sheet(date)
    result_dict = json.loads(result)
    assert result_dict["greeting"] == "Доброе утро"

    date = "2025-01-03 17:00:00"
    result = main_sheet(date)
    result_dict = json.loads(result)
    assert result_dict["greeting"] == "Добрый вечер"

    date = "2025-01-03 10:00:00"
    result = main_sheet(date)
    result_dict = json.loads(result)
    assert len(result_dict["cards"]) == 1
    assert len(result_dict["top_transactions"]) == 2
    assert result_dict["currency_rates"] == [{"USD": 90.1}, {"EUR": 98.7}]
    assert result_dict["stock_prices"] == [
        {"AAPL": 153.4},
        {"AMZN": 3421.5},
        {"GOOGL": 2720.2},
        {"MSFT": 299.1},
        {"TSLA": 721.3},
    ]
