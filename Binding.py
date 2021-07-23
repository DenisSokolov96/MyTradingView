import PySimpleGUI as sg
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import Parsing
from Assets import Assets
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


def get_portfolio():
    if len(assets.portfolio[0]) > 0:
        return assets.portfolio
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return parsing_for_portfolio(doc)


def parsing_for_portfolio(doc):
    list_values = []
    list_header = ['###', 'Бумага', 'Тикер', 'Количество', 'Инвестировано']
    portfolio = {}
    count = 0
    for element in reversed(doc.values):
        list_el = portfolio.get(element[4])
        if list_el is None:
            portfolio[element[4]] = [element[5], element[4], element[8], round(element[16], 2)]
        else:
            if element[7] == 'Покупка':
                portfolio[element[4]] = [element[5], element[4], element[8] + list_el[2],
                                         round(element[16] + list_el[3], 2)]
            else:
                portfolio[element[4]] = [element[5], element[4], list_el[2] - element[8],
                                         round(list_el[3] - element[16], 2)]
        count += 1

    for element in portfolio.values():
        if element[2] > 0:
            list_values.append(element)

    list_values.sort()
    count = 1
    for element in list_values:
        element.insert(0, count)
        count += 1
    assets.portfolio = [list_header, list_values]
    return list_header, list_values


def get_diagramma_circle():
    vals_money = []
    labels = []
    explode = []
    for element in assets.portfolio[1]:
        vals_money.append(element[4])
        labels.append(element[2])
        explode.append(0.3)

    fig, ax = plt.subplots()
    ax.pie(vals_money, labels=labels, explode=explode, rotatelabels=True)
    ax.axis("equal")
    plt.show()


def get_diagramma_column():
    vals_money = []
    labels = []
    for element in assets.portfolio[1]:
        vals_money.append(element[4])
        labels.append(element[2])
    colors = np.random.rand(10, 3)
    plt.xticks(rotation=45)
    plt.bar(labels, vals_money, color=colors)
    plt.show()
