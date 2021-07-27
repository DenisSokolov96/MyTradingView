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


# Получить российские акции: тикер | цена за штуку
def get_rus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off&iss.only="
        "marketdata&marketdata.columns=SECID,LAST")
    api_response = api_result.json()
    return api_response


# Получить зарубежные акции: тикер | цена за штуку
def get_unrus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/foreignshares/boards/FQBR/securities.json?iss.meta="
        "off&iss.only=marketdata&marketdata.columns=SECID,LAST")
    api_response = api_result.json()
    return api_response


# Получить ифо по российским акциям: тикер - название - лот
def get_info_rus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json?"
        "iss.meta=off&iss.only=securities&securities.columns=SECID,SHORTNAME,LOTSIZE")
    api_response = api_result.json()
    return api_response


# Получить ифо по зарубежным акциям: тикер - название - лот
def get_info_unrus_stock():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/foreignshares/boards/FQBR/securities.json?"
        "iss.meta=off&iss.only=securities&securities.columns=SECID,SHORTNAME,LOTSIZE")
    api_response = api_result.json()
    return api_response


# Получить облигации
def get_bonds_api():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/bonds/boardgroups/58/securities.json?"
        "iss.dp=comma&iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST")
    api_response = api_result.json()
    return api_response


# Получить названия облигаций
def get_name_bonds_api():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/bonds/boardgroups/58/securities.json?"
        "iss.dp=comma&iss.meta=off&iss.only=securities&securities.columns=SECID,SHORTNAME,"
        "COUPONPERCENT,NEXTCOUPON")
    api_response = api_result.json()
    return api_response


# Получить фонды
def get_pie_api():
    api_result = requests.get(
        "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQTF/securities.json"
        "?iss.dp=comma&iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST")
    api_response = api_result.json()
    return api_response


# Получить названия фондов
# def get_name_pie_api():
#     api_result = requests.get(
#         "https://iss.moex.com/iss/engines/stock/markets/bonds/boardgroups/58/securities.json?"
#         "iss.dp=comma&iss.meta=off&iss.only=securities&securities.columns=SECID,SHORTNAME,"
#         "COUPONPERCENT,NEXTCOUPON")
#     api_response = api_result.json()
#     return api_response

