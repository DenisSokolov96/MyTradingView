import PySimpleGUI as sg
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import Parsing
from Assets import Assets
from Handler import *
from Parsing import *

assets = Assets()


def load_menu():
    ftypes = [('Документы', '*.xlsx'), ('Документы', '*.xls'), ('Все файлы', '*')]
    dlg = sg.filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    if fl != '':
        df = pd.read_excel(fl)
        return df
    return


def create_graph():
    doc = Parsing.load_data(1)
    if doc is None:
        return
    count = len(doc['Операция']) - 1
    list_money = []
    lsit_sum = []
    sum = 0
    date = []
    while count > 0:
        if doc['Операция'][count] == 'Ввод ДС':
            sum += round(doc['Сумма'][count], 2)
            list_money.append(doc['Сумма'][count])
            lsit_sum.append(sum)
            d = datetime.strptime(str(doc['Дата исполнения поручения'][count]), '%Y-%m-%d %H:%M:%S')
            date.append(d.strftime("%d/%m/%y"))
        count -= 1
    plt.plot(date, list_money)
    plt.plot(date, lsit_sum)
    plt.title('Пополнение счета')
    plt.ylabel('Сумма')
    plt.xlabel('Дата')
    plt.xticks(rotation=90)
    plt.legend(['Внесение денежных средст', 'Увеличение общей суммы'], loc='upper left')
    plt.show()


def get_my_portfolio():
    if len(assets.portfolio[0]) > 0:
        return assets.portfolio
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return parsing_for_portfolio(doc)


def parsing_for_portfolio(doc):
    if len(assets.rus_stocks) == 0:
        get_ru()
    if len(assets.unrus_stocks) == 0:
        get_unru()

    list_values = []
    list_header = ['###', 'Компания', 'Бумага', 'Тикер', 'Количество', 'Инвестировано', 'Продано(шт)', 'Цена продажи',
                   'Цена за одну', 'Прибыль']
    portfolio = {}
    count = 0

    for element in reversed(doc.values):
        list_el = portfolio.get(element[4])
        if list_el is None:
            portfolio[element[4]] = [element[5], element[4], element[8], round(element[16], 2), 0, 0]
        else:
            if element[7] == 'Покупка':
                portfolio[element[4]] = [element[5], element[4], element[8] + list_el[2],
                                         round(element[16] + list_el[3], 2), list_el[4], list_el[5]]
            else:
                portfolio[element[4]] = [element[5], element[4], list_el[2],
                                         list_el[3], list_el[4] + element[8], round(list_el[5] + element[16], 2)]
        count += 1
    history_stocks = []
    for element in portfolio.values():
        if element[2] > element[4]:
            if element[4] > 0:
                medium = round(element[3] / element[2], 2)
                element[2] -= element[4]
                element[3] = medium * element[2]
                element.append(round(element[5]/element[4], 2))
                res = round(element[5] - element[4] * medium)
                res = round(res - res * 0.13, 2)
                element.append(res)
            list_values.append(element)
        else:
            element.append(round(element[5] / element[4], 2))
            res = round(element[5] - element[3], 2)
            res = round(res - res * 0.13, 2)
            element.append(res)
            history_stocks.append(element)

    list_values.sort()
    count = 1
    for element in list_values:
        element.insert(0, count)
        element.insert(1, get_name(element[2]))
        count += 1
    count = 1
    for element in history_stocks:
        element.insert(0, count)
        element.insert(1, get_name(element[2]))
        count += 1
    assets.portfolio = [list_header, list_values]
    assets.history_stocks = history_stocks
    return list_header, list_values


def get_name(tiker):
    for el in assets.rus_stocks:
        if el[1] == tiker:
            return el[0]
    for el in assets.unrus_stocks:
        if el[1] == tiker:
            return el[0]
    return ""


def get_diagramma_circle():
    vals_money = []
    labels = []
    explode = []
    for element in assets.portfolio[1]:
        vals_money.append(element[5])
        if element[1] == "":
            labels.append(element[3])
        else:
            labels.append(element[1])
        explode.append(0.3)

    fig, ax = plt.subplots()
    ax.pie(vals_money, labels=labels, explode=explode, rotatelabels=True)
    ax.axis("equal")
    plt.show()


def get_diagramma_column():
    vals_money = []
    labels = []
    for element in assets.portfolio[1]:
        vals_money.append(element[5])
        if element[1] == "":
            labels.append(element[3])
        else:
            labels.append(element[1])
    colors = np.random.rand(10, 3)
    plt.xticks(rotation=45)
    plt.bar(labels, vals_money, color=colors)
    plt.show()
