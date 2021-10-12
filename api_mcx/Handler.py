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
        list_news.append([d.strftime("%H:%M %d/%m/%Y"), news[2], news[0]])
    return list_news


# новость по id
def get_newtext_id(id):
    news = get_news_id(id)['content']['data'][0][3]
    soup = BeautifulSoup(news, "html.parser")
    for elm in soup(["script", "style"]):
        elm.extract()
    text = soup.get_text()
    return text


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
    list_columns = ['Название облигации', 'Компания', 'Цена %', 'Доход %', 'Выплата по бумаге']
    info_bonds = None
    bonds_price = get_bonds_api()

    info_bonds = get_name_bonds_api()

    # secid = [name]
    dict = {}
    if info_bonds is not None:
        for bonds in info_bonds['securities']['data']:
            dict[bonds[0]] = [bonds[1], 0, bonds[2], bonds[3]]
    else:
        dict = assets.bonds

    for bonds in bonds_price['marketdata']['data']:
        list = dict[bonds[0]]
        list[1] = bonds[1]
        dict[bonds[0]] = list

    list_data = []
    for k, v in dict.items():
        list_data.append([k, v[0], v[1], v[2], v[3]])

    assets.bonds = dict
    return list_data, list_columns, "Облигации"


# Обаботать фонды
def get_pies():
    list_columns = ['Наименование', 'Цена пая(р.)']
    pies_price = get_pie_api()

    dict = {}
    for pies in pies_price['marketdata']['data']:
        dict[pies[0]] = [pies[1]]

    list_data = []
    for k, v in dict.items():
        list_data.append([k, v[0]])

    assets.pies = dict
    return list_data, list_columns, "Фонды"
