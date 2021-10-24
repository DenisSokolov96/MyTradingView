import Parsing
from Assets import Assets
from Binding import check_none, handler_for_out
import api_mcx
from tools.StructRep import dict_pies

assets = Assets()


def parsing_pies_portfolio(doc):
    if len(assets.pies) == 0:
        api_mcx.Handler.get_pies()
    list_header = ['###', 'Наименование', 'Цена сейчас р.', 'Ср. цена', 'Изм. инвест. р.,', 'Инвестировано',
                   'Количество', 'Продано(шт.)', 'Продажа(р.)', '1 Пай(р.)', 'Фонд']
    portfolio_pies = {}
    for element in reversed(doc.values):
        if element[5] == 'Пай':
            if portfolio_pies.get(element[4]) is None:
                portfolio_pies[element[4]] = dict_pies.copy()
                portfolio_pies[element[4]]['name'] = element[4]
                portfolio_pies[element[4]]['count'] = element[8]
                portfolio_pies[element[4]]['invest'] = round(element[16], 2)
            else:
                if element[7] == 'Покупка':
                    portfolio_pies[element[4]]['count'] += element[8]
                    portfolio_pies[element[4]]['invest'] = round(portfolio_pies[element[4]]['invest'] + element[16], 2)
                else:
                    portfolio_pies[element[4]]['sold_count'] += element[8]
                    portfolio_pies[element[4]]['sold'] += round(element[16], 2)

    history_pies = {}
    count_value = 1
    count_history = 1
    for element_dict in portfolio_pies.values():
        element_dict['price_now'], element_dict['name_fond'] = get_price(element_dict['name'])
        if element_dict['count'] > element_dict['sold_count']:
            if element_dict['sold_count'] > 0:
                element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 2)

            element_dict['middle_price'] = round(element_dict['invest'] / element_dict['count'], 3)
            element_dict['change_invest'] = get_dif(element_dict['price_now'],
                                                    element_dict['count'], element_dict['invest'])
            element_dict['num'] = count_value
            count_value += 1
        else:
            element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 2)
            element_dict['num'] = count_history
            element_dict['middle_price'] = round(element_dict['invest'] / element_dict['count'], 3)
            element_dict['change_invest'] = get_dif(element_dict['price_now'],
                                                    element_dict['count'], element_dict['invest'])
            count_history += 1
            history_pies[element_dict['name']] = element_dict

    for element_dict in history_pies.values():
        del portfolio_pies[element_dict['name']]

    assets.portfolio_pies = [list_header, portfolio_pies]
    assets.history_pies = check_none(history_pies, len(list_header))

    return list_header, portfolio_pies


def get_my_pies():
    if len(assets.portfolio_pies[0]) > 0:
        return handler_for_out(assets.portfolio_pies)
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return handler_for_out(parsing_pies_portfolio(doc))


def get_name(tiker):
    tiker_info = assets.pies.get(tiker)
    if tiker_info is not None:
        return tiker_info[0]
    return ""


def get_dif(price, count, total):
    if price is None or count == '' or total == '':
        return "-"
    else:
        return round(price * count - total, 2)


def get_price(tiker):
    price = assets.pies.get(tiker)
    if price is not None:
        return price
    return ""