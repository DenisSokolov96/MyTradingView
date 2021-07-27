import numpy as np
import pandas as pd
import PySimpleGUI as sg
import Parsing

from datetime import datetime
from matplotlib import pyplot as plt
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


def get_diagramma_circle():
    labels, vals_money,  explode = scan_list(3)
    fig, ax = plt.subplots()
    ax.pie(vals_money, labels=labels, explode=explode, rotatelabels=True)
    ax.axis("equal")
    plt.show()


def get_diagramma_column():
    labels, vals_money = scan_list(2)
    colors = np.random.rand(10, 3)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.bar(labels, vals_money, color=colors)
    plt.show()


def scan_list(return_count_list):
    labels = []
    vals_money = []
    explode = []
    for element in assets.portfolio_stocks[1]:
        vals_money.append(element[7])
        if element[1] == "":
            labels.append(element[3])
        else:
            labels.append(element[1])
        explode.append(0.3)
    for element in assets.portfolio_bonds[1]:
        vals_money.append(element[4])
        if element[2] == "":
            labels.append(element[1])
        else:
            labels.append(element[2])
        explode.append(0.3)
    for element in assets.portfolio_pies[1]:
        vals_money.append(element[3])
        labels.append(element[1])
        explode.append(0.3)
    if return_count_list == 2:
        return labels, vals_money
    else:
        return labels, vals_money, explode


def check_none(history_list, count):
    if len(history_list) > 0:
        return history_list
    else:
        inner_list = []
        for i in range(0, count):
            inner_list.append('-')

        history_list.append(inner_list)
        return history_list