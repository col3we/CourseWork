import os
from unittest.mock import call, patch

from dotenv import load_dotenv

from src.external_api import get_currency, get_stocks


@patch("requests.get")
def test_get_currency_mock(mock_get, user_set):
    mock_get.return_value.json.return_value = {"success": True, "info": "some_info", "result": 90, "currency": "USD"}
    assert get_currency(user_set) == [{"currency": "USD", "rate": 90}, {"currency": "EUR", "rate": 90}]
    load_dotenv()
    CUR_API_KEY = os.getenv("CUR_API_KEY")

    expected_calls = [
        call(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1",
            headers={"apikey": CUR_API_KEY},
        ),
        call(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1",
            headers={"apikey": CUR_API_KEY},
        ),
    ]

    mock_get.assert_has_calls(expected_calls, any_order=True)


def test_get_currency():
    assert (get_currency({"user_currencies": ["apsidhaspda", "oasidoiasud"]})) == []


@patch("requests.get")
def test_get_stocks_mock(mock_get, user_set):
    mock_get.return_value.json.return_value = {"success": True, "info": "some_info", "price": 90, "stock": "USD"}
    assert get_stocks(user_set) == [
        {"stock": "AAPL", "price": 90},
        {"stock": "AMZN", "price": 90},
        {"stock": "GOOGL", "price": 90},
        {"stock": "MSFT", "price": 90},
        {"stock": "TSLA", "price": 90},
    ]
    load_dotenv()
    STC_API_KEY = os.getenv("STC_API_KEY")

    expected_calls = [
        call("https://api.api-ninjas.com/v1/stockprice?ticker={}".format("AAPL"), headers={"X-Api-Key": STC_API_KEY}),
        call("https://api.api-ninjas.com/v1/stockprice?ticker={}".format("AMZN"), headers={"X-Api-Key": STC_API_KEY}),
        call("https://api.api-ninjas.com/v1/stockprice?ticker={}".format("GOOGL"), headers={"X-Api-Key": STC_API_KEY}),
        call("https://api.api-ninjas.com/v1/stockprice?ticker={}".format("MSFT"), headers={"X-Api-Key": STC_API_KEY}),
        call("https://api.api-ninjas.com/v1/stockprice?ticker={}".format("TSLA"), headers={"X-Api-Key": STC_API_KEY}),
    ]

    mock_get.assert_has_calls(expected_calls, any_order=True)


def test_get_stocks():
    assert (get_stocks({"user_stocks": ["apsidhaspda", "oasidoiasud", "asdfsad", "asdasd", "asdasdad"]})) == []
