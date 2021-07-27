import Parsing
from Assets import Assets
from Binding import check_none
import api_mcx

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_stocks[0]) > 0:
        return assets.portfolio_stocks
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return parsing_for_portfolio(doc)


def parsing_for_portfolio(doc):
    if len(assets.rus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('ru')
    if len(assets.unrus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('unru')

    list_values = []
    list_header = ['###', 'Компания', 'Бумага', 'Тикер', 'Цена акции сейчас р.', 'Изменение инвестиций р.', 'Количество',
                   'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.', 'Цена за одну р.', 'Прибыль р.']
    portfolio_stocks = {}

    for element in reversed(doc.values):
        if element[5] == 'Акция' or element[5] == 'Депозитарная расписка':
            list_el = portfolio_stocks.get(element[4])
            if list_el is None:
                portfolio_stocks[element[4]] = [element[5], element[4], element[8], round(element[16], 2), 0, 0, 0, 0]
            else:
                if element[7] == 'Покупка':
                    portfolio_stocks[element[4]] = [element[5], element[4], element[8] + list_el[2],
                                             round(element[16] + list_el[3], 2), list_el[4], list_el[5], 0, 0]
                else:
                    portfolio_stocks[element[4]] = [element[5], element[4], list_el[2],
                                             list_el[3], list_el[4] + element[8], round(list_el[5] + element[16], 2),
                                                    0, 0]

    history_stocks = []
    for element in portfolio_stocks.values():
        if element[2] > element[4]:
            if element[4] > 0:
                medium = round(element[3] / element[2], 2)
                element[2] -= element[4]
                element[3] = medium * element[2]
                element[6] = round(element[5]/element[4], 2)
                res = round(element[5] - element[4] * medium)
                res = round(res - res * 0.13, 2)
                element[7] = res
            list_values.append(element)
        else:
            element[6] = round(element[5] / element[4], 2)
            res = round(element[5] - element[3], 2)
            res = round(res - res * 0.13, 2)
            element[7] = res
            history_stocks.append(element)

    list_values.sort()
    count = 1
    for element in list_values:
        element.insert(0, count)
        element.insert(1, get_name(element[2]))
        element.insert(4, get_price(element[3]))
        element.insert(5, get_dif(element[4], element[5], element[6]))
        count += 1

    count = 1
    for element in history_stocks:
        element.insert(0, count)
        element.insert(1, get_name(element[2]))
        element.insert(4, get_price(element[3]))
        element.insert(5, get_dif(element[4], element[5], element[6]))

        count += 1
    assets.portfolio_stocks = [list_header, list_values]
    assets.history_stocks = check_none(history_stocks, len(list_header))
    return list_header, list_values


def get_name(tiker):
    stock_info = assets.rus_stocks.get(tiker)
    if stock_info is not None:
        return stock_info[0]
    stock_info = assets.unrus_stocks.get(tiker)
    if stock_info is not None:
        return stock_info[0]
    return ""


def get_price(tiker):
    stock_info = assets.rus_stocks.get(tiker)
    if stock_info is not None:
        return stock_info[2]
    stock_info = assets.unrus_stocks.get(tiker)
    if stock_info is not None:
        return stock_info[2]
    return ""


def get_dif(price, count, total):
    if price == '' or count == '' or total == '':
        return ""
    else:
        return round(price * count - total, 2)