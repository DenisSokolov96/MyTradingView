import numpy as np
import pandas as pd
import PySimpleGUI as sg
import Parsing
import tools

from Assets import Assets
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
    plt.gcf().canvas.set_window_title('Изменение общей суммы')
    plt.plot(date, list_money)
    plt.plot(date, lsit_sum)
    plt.title('Пополнение счета')
    plt.ylabel('Сумма')
    plt.xlabel('Дата')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    plt.legend(['Внесение денежных средст', 'Увеличение общей суммы'], loc='upper left')
    plt.show()


def get_diagramma_circle():
    labels, vals_money, explode = scan_list(3)
    fig, ax = plt.subplots()
    ax.pie(vals_money, labels=labels, explode=explode, rotatelabels=True)
    ax.axis("equal")
    fig.canvas.set_window_title('Круговая диаграмма')
    plt.show()


def get_diagramma_column():
    labels, vals_money = scan_list(2)
    colors = np.random.rand(10, 3)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.bar(labels, vals_money, color=colors)
    fig = plt.gcf()
    fig.canvas.set_window_title('Столбчатая диаграмма')
    plt.show()


def scan_list(return_count_list):
    labels = []
    vals_money = []
    explode = []
    for element in assets.portfolio_stocks[1].values():
        vals_money.append(element['invest'])
        labels.append(element['company'])
        explode.append(0.2)
    for element in assets.portfolio_bonds[1].values():
        vals_money.append(element['invest'])
        labels.append(element['company'])
        explode.append(0.2)
    for element in assets.portfolio_pies[1].values():
        vals_money.append(element['invest'])
        labels.append(element['name'])
        explode.append(0.2)
    if return_count_list == 2:
        return labels, vals_money
    else:
        return labels, vals_money, explode


def check_none(history_list, count):
    if len(history_list) > 0:
        return history_list
    else:
        history_list['none'] = {}
        for i in range(0, count):
            history_list['none'][i] = '-'
    return history_list


def get_diagramma_compos():
    labels = ['Акции', 'Облигации', 'Фонды']
    vals_money = get_compos()
    write_diagramm(labels, vals_money, 'Состав портфеля по категориям')


def get_compos():
    vals_money = []

    sum = 0
    for element in assets.portfolio_stocks[1].values():
        sum += element['invest']
    vals_money.append(round(sum, 2))

    sum = 0
    for element in assets.portfolio_bonds[1].values():
        sum += element['invest']
    vals_money.append(round(sum, 2))

    sum = 0
    for element in assets.portfolio_pies[1].values():
        sum += element['invest']
    vals_money.append(round(sum, 2))

    return vals_money


def get_rus_unrus_stocks():
    labels = ['Зарубежные акции', 'Российские акции', 'Депозитарные расписки']
    vals_money = get_stocks_all()
    write_diagramm(labels, vals_money, 'Виды акций')


def get_stocks_all():
    vals_money = [0, 0, 0]
    for element in assets.portfolio_stocks[1].values():
        if element['paper'] == 'Деп. рас.':
            vals_money[2] += element['invest']
        elif element['tiker'].find('-RM') != -1:
            vals_money[0] += element['invest']
        else:
            vals_money[1] += element['invest']

    for i in range(0, len(vals_money)):
        vals_money[i] = round(vals_money[i], 2)

    return vals_money


def get_all_pies():
    labels = []
    vals_money = []
    for element in assets.portfolio_pies[1].values():
        labels.append(element['name'])
        vals_money.append(element['invest'])
    write_diagramm(labels, vals_money, 'Состав фондов')


def get_all_bonds():
    labels = []
    vals_money = []
    for element in assets.portfolio_bonds[1].values():
        labels.append(element['company'])
        vals_money.append(element['invest'])
    write_diagramm(labels, vals_money, 'Виды облигаций')


def get_name_stocks():
    labels = []
    vals_money = []
    for element in assets.portfolio_stocks[1].values():
        labels.append(element['company'])
        vals_money.append(element['invest'])
    write_diagramm(labels, vals_money, 'Акции в портфеле')


def write_diagramm(labels, vals_money, text_header):
    for i in range(0, len(labels)):
        labels[i] += '\n(' + str(vals_money[i]) + 'р.)'
    fig, ax = plt.subplots()
    ax.pie(vals_money, labels=labels, autopct='%1.2f%%', rotatelabels=True,
           wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"})
    ax.axis("equal")
    fig.canvas.set_window_title(text_header)
    plt.show()


def handler_for_out(data):
    list_header = data[0]
    list_value = []

    for dict in data[1].values():
        temp = []
        for val in dict.values():
            temp.append(val)
        list_value.append(temp)

    return list_header, list_value


def to_list(data):
    new_list = []
    for element_dict in data.values():
        temp = []
        for el in element_dict.values():
            temp.append(el)
        new_list.append(temp)
    return new_list


def redact(text):
    page = text.replace("\n\n", "\n")
    return page


def search(list_data, str_search, info):
    if info.find('акции') > -1:
        return for_stocks(list_data, str_search)
    if info.find('Облигации') > -1:
        return for_bonds(list_data, str_search)
    if info.find('Фонды') > -1:
        return for_pies(list_data, str_search)
    return ""


def for_stocks(list_data, str_search):
    list_stocks = []
    for el in list_data:
        if el[0].find(str_search) > -1 or el[1].find(str_search) > -1:
            s = el[1] + " " + el[0] + " " + str(el[2]) + "р. " + str(el[3]) + "шт. в лоте"
            list_stocks.append(s)
    return list_stocks


def for_bonds(list_data, str_search):
    list_bonds = []
    for el in list_data:
        if el[0].find(str_search) > -1 or el[1].find(str_search) > -1:
            s = el[1] + " " + str(el[2]) + "%цена " + str(el[3]) + "%доход " + el[0]
            list_bonds.append(s)
    return list_bonds


def for_pies(list_data, str_search):
    list_pies = []
    for el in list_data:
        if el[0].find(str_search) > -1:
            s = el[0] + " " + str(el[1]) + "р. пай"
            list_pies.append(s)
    return list_pies


def report_invest():
    list_values_stocks = tools.Stocks.get_my_portfolio()[1:]
    list_values_bonds = tools.Bonds.get_my_bonds()[1:]
    list_values_pies = tools.Pie.get_my_pies()[1:]

    list_headers = ['Ценная бумага', 'Инвестированно', 'Оценка активов сейчас', 'Изменение в р.', 'Изменение в %']
    list_data = []
    # Акции------------------------------------------------------------------------
    invest = 0.0
    price_now = 0.0
    invest_us = 0.0
    price_now_us = 0.0
    for i in range(0, len(list_values_stocks[0])):
        if list_values_stocks[0][i][13] != "США":
            invest += list_values_stocks[0][i][8]
            if type(list_values_stocks[0][i][6]) is float:
                price_now += list_values_stocks[0][i][8] + list_values_stocks[0][i][6]
        else:
            invest_us += list_values_stocks[0][i][8]
            if type(list_values_stocks[0][i][6]) is float:
                price_now_us += list_values_stocks[0][i][8] + list_values_stocks[0][i][6]
    invest = round(invest, 2)
    price_now = round(price_now, 2)
    list_data.append(['Российские акции', invest, price_now,
                      round(price_now - invest, 2), str(round(price_now * 100 / invest - 100, 2)) + " %"])
    invest_us = round(invest_us, 2)
    price_now_us = round(price_now_us, 2)
    list_data.append(['Зарубежные акции', invest_us, price_now_us,
                      round(price_now_us - invest_us, 2), str(round(price_now_us * 100 / invest_us - 100, 2)) + " %"])
    # Облигации------------------------------------------------------------------------
    invest = 0.0
    price_now = 0.0
    for i in range(0, len(list_values_bonds[0])):
        invest += list_values_bonds[0][i][6]
        if type(list_values_bonds[0][i][5]) is float:
            price_now += list_values_bonds[0][i][6] + list_values_bonds[0][i][5]
    invest = round(invest, 2)
    price_now = round(price_now, 2)
    list_data.append(['Облигации', invest, price_now, round(price_now - invest, 2),
                      str(round(price_now * 100 / invest - 100, 2)) + " %"])
    # ETF фонды-------------------------------------------------------------------------
    invest = 0.0
    price_now = 0.0
    for i in range(0, len(list_values_pies[0])):
        invest += list_values_pies[0][i][5]
        if type(list_values_pies[0][i][4]) is float:
            price_now += list_values_pies[0][i][5] + list_values_pies[0][i][4]
    invest = round(invest, 2)
    price_now = round(price_now, 2)
    list_data.append(['ETF фонды', invest, price_now, round(price_now - invest, 2),
                      str(round(price_now * 100 / invest - 100, 2)) + " %"])

    invest = 0.0
    price_now = 0.0
    for i in range(0, len(list_data)):
        invest += list_data[i][1]
        price_now += list_data[i][2]

    list_data.append(['Итог', round(invest, 2), round(price_now, 2), round(price_now - invest, 2),
                      str(round(price_now * 100 / invest - 100, 2)) + " %"])

    list_colors = []
    for i in range(0, len(list_data)):
        if list_data[i][3] > 0:
            list_colors.append([i, "green", "lightblue" if i % 2 else "white"])

    return list_headers, list_data, list_colors


# График вывода истории акции
def create_history_graph(list_data, list_price, text_header):
    plt.gcf().canvas.set_window_title(text_header)
    plt.plot(list_data, list_price)
    plt.title('Потоковый график')
    plt.ylabel('Цена р.')
    plt.xlabel('Дата')
    plt.xticks(list_data[::15], rotation=45)
    plt.grid(axis='y')
    plt.show()


# поиск индекса бумаги в списке
def search_index(name, list_data, info):
    if info.find('акции') > -1:
        for i in range(0, len(list_data)):
            if list_data[i][1].find(name) == 0:
                return i
    if info.find('Фонды') > -1:
        for i in range(0, len(list_data)):
            if list_data[i][0].find(name) == 0:
                return i
    if info.find('Облигации') > -1:
        for i in range(0, len(list_data)):
            if list_data[i][0].find(name) == 0:
                return i
    return 0
