from tabulate import tabulate

from API_response import *

list_news = []


# список новостей
def get_list_news():
    for news in get_news()['sitenews']['data']:
        list_news.append(news)

    for element in list_news:
        date = element[3].split(" ")
        print(date[0] + " " + element[2])

# новость по id
#def get_news_id():
#    for news in API_response.get_news_id(news_id)['sitenews']['data']:


# Получить российскте акции
def get_ru():
    list_data = []
    data = get_rus_stock()
    list_columns = rename_col(data['securities']['columns'])
    for stock in data['securities']['data']:
        list_data.append(stock)
    return list_data, list_columns, "Российские акции"


# Получить зарубежные акции
def get_unru():
    list_data = []
    data = get_unrus_stock()
    list_columns = rename_col(data['securities']['columns'])
    for stock in data['securities']['data']:
        list_data.append(stock)
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