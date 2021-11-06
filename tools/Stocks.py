import Parsing
from Assets import Assets
from Binding import check_none, handler_for_out
from tools.StructRep import dict_stocks
import api_mcx

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_stocks[0]) > 0:
        return handler_for_out(assets.portfolio_stocks)
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return handler_for_out(parsing_for_portfolio(doc))


def parsing_for_portfolio(doc):
    if len(assets.rus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('ru')
    if len(assets.unrus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('unru')

    list_header = ['###', 'Компания', 'Бумага', 'Тикер', 'Цена сейчас р.', 'Ср. цена',
                   'Изм. инвест. р.', 'Кол - во', 'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.',
                   'Цена за одну р.', 'Прибыль р.', 'Страна']
    portfolio_stocks = {}
    for element in reversed(doc.values):
        if element[5] == 'Акция' or element[5] == 'Депозитарная расписка':
            if portfolio_stocks.get(element[4]) is None:
                portfolio_stocks[element[4]] = dict_stocks.copy()
                portfolio_stocks[element[4]]['tiker'] = element[4]
                portfolio_stocks[element[4]]['count'] = element[8]
                portfolio_stocks[element[4]]['invest'] = round(element[16], 2)
                if element[5] == 'Депозитарная расписка':
                    portfolio_stocks[element[4]]['paper'] = 'Деп. рас.'
                    portfolio_stocks[element[4]]['country'] = 'Др. стр.'
                if element[5] == 'Акция':
                    portfolio_stocks[element[4]]['paper'] = 'Акция'
                    if portfolio_stocks[element[4]]['tiker'].find('-RM') != -1:
                        portfolio_stocks[element[4]]['country'] = 'США'
                    else:
                        portfolio_stocks[element[4]]['country'] = 'Рос.'
            else:
                if element[7] == 'Покупка':
                    portfolio_stocks[element[4]]['count'] += element[8]
                    portfolio_stocks[element[4]]['invest'] = round(portfolio_stocks[element[4]]['invest'] +
                                                                   element[16], 2)
                else:
                    portfolio_stocks[element[4]]['sold_count'] += element[8]
                    portfolio_stocks[element[4]]['sold'] = round(portfolio_stocks[element[4]]['sold'] + element[16], 2)
                    portfolio_stocks[element[4]]['price_sold'] = round(portfolio_stocks[element[4]]['invest'] /
                                                                       portfolio_stocks[element[4]]['count'], 2)

    history_stocks = {}
    count_value = 1
    count_history = 1

    for element_dict in portfolio_stocks.values():
        element_dict['company'] = get_name(element_dict['tiker'])
        element_dict['price_now'] = get_price(element_dict['tiker'])
        if element_dict['count'] > element_dict['sold_count']:
            if element_dict['sold_count'] > 0:
                medium = round(element_dict['invest'] / element_dict['count'], 2)
                element_dict['count'] -= element_dict['sold_count']
                element_dict['invest'] = medium * element_dict['count']
                medium_to_sold = element_dict['price_sold']
                element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 2)
                res = round(element_dict['sold'] - element_dict['sold_count'] * medium_to_sold, 2)
                res = round(res - res * 0.13, 2)
                element_dict['income'] = res

            element_dict['middle_price'] = round(element_dict['invest'] / element_dict['count'], 3)
            element_dict['change_invest'] = get_dif(element_dict['price_now'],
                                                    element_dict['count'], element_dict['invest'])
            element_dict['num'] = count_value
            count_value += 1
        else:
            element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 3)
            res = round(element_dict['sold'] - element_dict['invest'], 3)
            res = round(res - res * 0.13, 2)
            element_dict['income'] = res
            element_dict['middle_price'] = round(element_dict['invest'] / element_dict['count'], 3)
            element_dict['change_invest'] = get_dif(element_dict['price_now'],
                                                    element_dict['count'], element_dict['invest'])
            element_dict['num'] = count_history
            count_history += 1
            history_stocks[element_dict['tiker']] = element_dict

    for element_dict in history_stocks.values():
        del portfolio_stocks[element_dict['tiker']]

    assets.portfolio_stocks = [list_header, portfolio_stocks]
    assets.history_stocks = check_none(history_stocks, len(list_header))
    return list_header, portfolio_stocks


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
    if price is None or count == '' or total == '':
        return '-'
    else:
        return round(price * count - total, 2)
