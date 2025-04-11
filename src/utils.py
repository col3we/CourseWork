import logging
import os
from typing import Any, Hashable, Union

import pandas as pd

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "utils.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def XLSX_file_read() -> Union[list[dict[Hashable, Any]], str]:
    """Возвращает json список словарей со всеми транзакциями"""
    logger.info("Задаём путь до файла")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_path = os.path.join(data_dir, "operations.xlsx")
    logger.info("Переводим XLSX файл в json формат")
    df = pd.read_excel(file_path)
    fixed_df = df.dropna(subset=["Номер карты"])
    list_of_dicts = fixed_df.to_dict(orient="records")
    return list_of_dicts


def file_df():
    """Возвращает DataFrame со списком словарей со всеми транзакциями"""
    logger.info("Задаём путь до файла")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_path = os.path.join(data_dir, "operations.xlsx")
    logger.info("Переводим XLSX файл в DataFrame формат")
    df = pd.read_excel(file_path)
    fixed_df = df.dropna(subset=["Номер карты"])
    return fixed_df
