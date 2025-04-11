import os

import pandas as pd
import pytest

from src.reports import report_file_write, spending_by_category
from src.utils import file_df


def test_report_file():
    filename = "test.txt"
    my_pd = pd.DataFrame({"Yes": [50, 21], "No": [131, 2]})

    @report_file_write(filename=filename)
    def test_function(my_pd_1):
        return my_pd_1

    test_function(my_pd)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(base_dir, "..", "reports")
    file_path = os.path.join(dir, filename)
    text = open(file_path, "r")
    assert (
        text.read()
        == """   Yes   No
0   50  131
1   21    2"""
    )


data = file_df()


@pytest.mark.parametrize(
    "transactions, category, date, expected",
    [
        (data, "Супермаркеты", "2021-11-15", {"Супермаркеты": -33092.63}),
        (data, "Переводы", "2021-12-15", {"Переводы": -25800.0}),
        (data, "Пополнения", "2021-01-15", {"Пополнения": 0}),
        (data, "Пополнения", None, {"Пополнения": 0}),
    ],
)
def test_spending_by_category(transactions, category, date, expected):
    assert spending_by_category(transactions, category, date) == expected
