import base64
import webbrowser

from api_mcx.API_response import *
from datetime import datetime
from bs4 import BeautifulSoup

from Assets import Assets

assets = Assets()


# список новостей
def get_list_news():
    list_news = []
    for news in get_news()['sitenews']['data']:
        d = datetime.strptime(news[3], '%Y-%m-%d %H:%M:%S')
        list_news.append([d.strftime("%H:%M %d/%m/%y"), news[2], news[0]])
    return list_news


# новость по id
# def get_newtext_id(id):
#     news = get_news_id(id)['content']['data'][0][3]
#     soup = BeautifulSoup(news, "html.parser")
#     for elm in soup(["script", "style"]):
#         elm.extract()
#     text = soup.get_text()
#     return text


# Получить акции
def get_stocks_15m_ago(name_country):
    list_columns = ['Название компании', 'Тикер', 'Цена р.(1 шт.)', 'Акций в лоте']
    tiker_price = None
    info_stocks = None
    if name_country == 'ru':
        tiker_price = get_rus_stock()
        info_stocks = get_info_rus_stock()
    if name_country == 'unru':
        tiker_price = get_unrus_stock()
        info_stocks = get_info_unrus_stock()

    # secid = [name, lotsize, price]
    dict = {}
    if info_stocks is not None:
        for stock in info_stocks['securities']['data']:
            dict[stock[0]] = [stock[1], stock[2]]
        for stock in tiker_price['marketdata']['data']:
            dict[stock[0]].append(stock[1])
    else:
        if name_country == 'ru':
            dict = assets.rus_stocks
        if name_country == 'unru':
            dict = assets.unrus_stocks
        for stock in tiker_price['marketdata']['data']:
            list = dict[stock[0]]
            list[2] = stock[1]
            dict[stock[0]] = list

    list_data = []
    for k, v in dict.items():
        list_data.append([v[0], k, v[2], v[1]])

    if name_country == 'ru':
        assets.rus_stocks = dict
        return list_data, list_columns, "Российские акции"
    if name_country == 'unru':
        assets.unrus_stocks = dict
        return list_data, list_columns, "Зарубежные акции"
    return


# Обаботать облигации
def get_bonds():
    list_columns = ['Название облигации', 'Компания', 'Цена %', 'НКД сейчас', 'Доход %', 'Выплата по бумаге']
    info_bonds = None
    bonds_price = get_bonds_api()

    info_bonds = get_name_bonds_api()

    # secid = [name]
    dict = {}
    if info_bonds is not None:
        for bonds in info_bonds['securities']['data']:
            if bonds[2] is not None:
                str_time = datetime.strptime(bonds[3], '%Y-%m-%d').strftime('%d/%m/%Y')
                dict[bonds[0]] = [bonds[1], 0, bonds[4], bonds[2], str_time]
    else:
        dict = assets.bonds

    for bonds in bonds_price['marketdata']['data']:
        if bonds[1] is not None and bonds[0] in dict:
            list = dict[bonds[0]]
            list[1] = bonds[1]
            dict[bonds[0]] = list

    list_data = []
    for k, v in dict.items():
        list_data.append([k, v[0], v[1], v[2], v[3], v[4]])

    assets.bonds = dict
    return list_data, list_columns, "Облигации"


# Обработать фонды
def get_pies():
    list_columns = ['Наименование', 'Цена пая(р.)', 'Фонд']
    pies_price = get_pie_api()
    pies_name = get_name_pie_api()

    dict = {}
    for pies in pies_price['marketdata']['data']:
        dict[pies[0]] = [pies[1], ""]
    for pies in pies_name['securities']['data']:
        dict[pies[0]][1] = pies[1]

    list_data = []
    for k, v in dict.items():
        list_data.append([k, v[0], v[1]])

    assets.pies = dict
    return list_data, list_columns, "Фонды"


# Курсы валют
def get_securities_rates():
    data = get_cbrf_api()
    str_date = "Валютный курс обнавлен: " + \
               datetime.strptime(data['securities']['data'][0][0], '%Y-%m-%d').strftime('%d/%m/%Y')
    mas = data['securities']['data'][0][1].split(':')
    str_date += " " + mas[0] + ":" + mas[1]
    str_value = ""
    for el in data['securities']['data']:
        if el[2].find('RUB') > -1:
           str_value += el[2].split('/RUB')[0] + " - " + str(round(el[3], 2)) + " р.  "
    return str_date, str_value


# Обработать запрос на дивиденды по тикеру
def get_dividends(tiker):
    response = get_dividends_rus_api(tiker)
    list_dividends = []
    for el in response['dividends']['data']:
        list_dividends.append([round(el[3], 3), el[2], el[4]])
    if len(list_dividends) == 0:
        list_dividends.append(['', '', ''])
    else:
        list_dividends.reverse()

    return list_dividends


# Обработать запрос по будующим выплатам НКД
def get_all_nkd(tiker):
    response = get_all_nkd_api(tiker)
    list = []
    for el in response['coupons']['data']:
        el[0] = datetime.strptime(el[0], '%Y-%m-%d').strftime('%d/%m/%Y')
        list.append([el[0], el[1], el[2]])
    list.reverse()
    return list


# Обработать запрос на историю Российских акций
def get_history_stocks(tiker, info):
    now = datetime.now()
    delta = timedelta(days=100)
    date = (now - delta).strftime('%Y-%m-%d')
    res_data = []
    res_price_history = []
    last_date = now + timedelta(days=1)

    for i in range(0, 5):
        list_data = []
        list_price_history = []
        if info == "rus":
            response = get_history_rus_prices_api(tiker, date)
        else:
            response = get_history_unrus_prices_api(tiker, date)
        for el in response['history']['data']:
            if el[1] is not None and el[2] != "TQBD":
                el[0] = datetime.strptime(el[0], '%Y-%m-%d')
                if last_date > el[0]:
                    list_data.append(el[0])
                    list_price_history.append(el[1])

        if len(list_data) > 0:
            mas = str(list_data[0]).split(' ')
            last_date = datetime.strptime(mas[0], '%Y-%m-%d')
            date = (datetime.strptime(date, '%Y-%m-%d') - delta).strftime('%Y-%m-%d')
            res_data = list_data + res_data
            res_price_history = list_price_history + res_price_history

    for i in range(0, len(res_data)):
        res_data[i] = datetime.strptime(str(res_data[i]).split(' ')[0], '%Y-%m-%d').strftime('%d/%m/%y')

    return res_data, res_price_history


def get_trade_system():
    response = get_trade_system_api()
    list_value = []
    for el in response['engines']['data']:
        list_value.append([el[0], el[2]])
    return list_value


def get_turnovers():
    response = get_turnovers_api()
    list_today = []
    list_yesterday = []
    for el in response['turnovers']['data']:
        str_date = datetime.strptime(el[5], '%Y-%m-%d %H:%M:%S').strftime("%H:%M %d/%m/%y")
        if el[2] is not None and el[3] is not None:
            list_today.append([el[6], el[4], round(el[2], 2), round(el[3], 2), str_date])
        else:
            list_today.append([el[6], el[4], el[2], el[3], str_date])

    for el in response['turnoversprevdate']['data']:
        str_date = datetime.strptime(el[5], '%Y-%m-%d %H:%M:%S').strftime("%H:%M %d/%m/%y")
        if el[2] is not None and el[3] is not None:
            list_yesterday.append([el[6], el[4], round(el[2], 2), round(el[3], 2), str_date])
        else:
            list_yesterday.append([el[6], el[4], el[2], el[3], str_date])
    return list_today, list_yesterday