"""
*for marketstack*
    params = {
        'access_key': 'my_key',
        'symbols': 'GLTR'
    }
    api_result = requests.get("http://api.marketstack.com/v1/tickers/UPRO/eod", params)

*for MOEX*
    "http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.json?date=2021-07-16"
"""

import requests


# новости биржи
def get_news():
    api_result = requests.get("http://iss.moex.com/iss/sitenews.json")
    api_response = api_result.json()
    return api_response


# для новостей сайта указать id
def get_news_id(news_id):
    api_result = requests.get("http://iss.moex.com/iss/sitenews/" + str(news_id) + ".json")
    api_response = api_result.json()
    return api_response


# Получить российскте акции: бумага | тикер | цена за штуку
def get_rus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off&iss.only="
        "securities&securities.columns=SHORTNAME,SECID,PREVADMITTEDQUOTE")
    api_response = api_result.json()
    return api_response


# Получить зарубежные акции: бумага | тикер | цена за штуку
def get_unrus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/foreignshares/boards/FQBR/securities.json?iss.meta="
        "off&iss.only=securities&securities.columns=SHORTNAME,SECID,PREVADMITTEDQUOTE")
    api_response = api_result.json()
    return api_response











def test4():
    # Получить данные по конкретному инструменту рынка
    api_result = requests.get("https://iss.moex.com/iss/engines/stock/markets/shares/securities/MTSS.json")
    api_response = api_result.json()
    print(api_response)


def test5():
    # / iss / securities / [security] / indices
    # Список индексов в которые входит бумага
    return

def test8():
    # Текущие цены бумаг
    # Например: /iss/statistics/engines/stock/currentprices
    api_result = requests.get("http://iss.moex.com/iss/statistics/engines/stock/currentprices.json")
    api_response = api_result.json()
    print(api_response)
    return


# if __name__ == '__main__':
#     get_norus_stock()
