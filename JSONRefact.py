import json

import PySimpleGUI as sg
import pandas as pd
import orjson

from AppLogger import file_logger
from Assets import Assets

assets = Assets()
path_to_file = 'data/UserInfo.json'


# Прочитать из JSON пути для парсинга файлов брокера
def load_json_files():
    try:
        with open(path_to_file, mode="r", encoding="utf-8") as f:
            data = orjson.loads(f.read())

        if data["deals"] is not None:
            assets.doc_deals = pd.read_excel(data["deals"][0])
        if data["transactions"] is not None:
            assets.doc_transactions = pd.read_excel(data["transactions"][0])

        file_logger.info("файл прочитан")

    except FileNotFoundError:
        file_logger.error("Файл не найден...")


# Открыть проводник
def set_path(name_doc):
    ftypes = [('Документы по' + name_doc, '*.xlsx'), ('Документы', '*.xls'), ('Все файлы', '*')]
    dlg = sg.filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    if fl != '':
        return fl
    return ''


# Запись путей к файлу для парсинга в XML
def write_to_json(path_deals, path_trans):
    try:
        newJson = {
            "deals": [path_deals],
            "transactions": [path_trans]
        }
        with open(path_to_file, "w") as f:
            json.dump(newJson, f)
    except FileNotFoundError:
        file_logger.error("Файл не найден...")
    load_json_files()
