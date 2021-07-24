from API_response import *
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


# Получить российскте акции
def get_ru():
    list_data = []
    data = get_rus_stock()
    list_columns = rename_col(data['securities']['columns'])
    for stock in data['securities']['data']:
        list_data.append(stock)

    if len(assets.rus_stocks) == 0:
        list_short = []
        for el in list_data:
            list_short.append(el[0:2])
        assets.rus_stocks = list_short

    return list_data, list_columns, "Российские акции"


# Получить зарубежные акции
def get_unru():
    list_data = []
    data = get_unrus_stock()
    list_columns = rename_col(data['securities']['columns'])
    for stock in data['securities']['data']:
        list_data.append(stock)

    if len(assets.unrus_stocks) == 0:
        list_short = []
        for el in list_data:
            list_short.append(el[0:2])
        assets.unrus_stocks = list_short

    return list_data, list_columns, "Зарубежные акции"


def rename_col(list_columns):
    list_en = ['SHORTNAME', 'SECID', 'PREVADMITTEDQUOTE', 'MINSTEP']  # PREVWAPRICE или PREVADMITTEDQUOTE
    list_ru = ['Сокр. название', 'Тикер', 'Цена р.', 'Шаг изменения цены']
    count = 0
    while count < len(list_columns):
        for el in range(0, len(list_en)):
            if list_en[el] == list_columns[count]:
                list_columns[count] = list_ru[el]
                break
        count += 1
    return list_columns