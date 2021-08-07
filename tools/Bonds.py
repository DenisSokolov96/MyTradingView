import Parsing
from Assets import Assets
from Binding import check_none, handler_for_out
from tools.StructRep import dict_bonds
import api_mcx

assets = Assets()


def parsing_bonds_portfolio(doc):
    if len(assets.bonds) == 0:
        api_mcx.Handler.get_bonds()
    list_header = ['###', 'Наименование', 'Компания', 'Количество', 'Инвестировано', 'Доход %',
                   'Продано(шт.)', 'Продажа(р.)', '1 Бонд(р.)']
    portfolio_bonds = {}
    for element in reversed(doc.values):
        if element[5] == 'Облигация':
            if portfolio_bonds.get(element[4]) is None:
                portfolio_bonds[element[4]] = dict_bonds.copy()
                portfolio_bonds[element[4]]['name'] = element[4]
                portfolio_bonds[element[4]]['count'] = element[8]
                portfolio_bonds[element[4]]['invest'] = round(element[16], 2)
            else:
                if element[7] == 'Покупка':
                    portfolio_bonds[element[4]]['count'] += element[8]
                    portfolio_bonds[element[4]]['invest'] += round(element[16], 2)
                else:
                    portfolio_bonds[element[4]]['sold_count'] += element[8]
                    portfolio_bonds[element[4]]['sold'] += round(element[16])

    history_bonds = {}
    count_value = 1
    count_history = 1
    for element_dict in portfolio_bonds.values():
        if element_dict['count'] > element_dict['sold_count']:
            if element_dict['sold_count'] > 0:
                element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 2)
            element_dict['num'] = count_value
            element_dict['company'] = get_name(element_dict['name'])
            element_dict['income'] = get_income(element_dict['name'])
            count_value += 1
        else:
            element_dict['price_sold'] = round(element_dict['sold'] / element_dict['sold_count'], 2)
            element_dict['num'] = count_history
            element_dict['company'] = get_name(element_dict['name'])
            count_history += 1
            history_bonds[element_dict['name']] = element_dict

    for element_dict in history_bonds.values():
        del portfolio_bonds[element_dict['name']]

    assets.portfolio_bonds = [list_header, portfolio_bonds]
    assets.history_bonds = check_none(history_bonds, len(list_header))
    return list_header, portfolio_bonds


def get_my_bonds():
    if len(assets.portfolio_bonds[0]) > 0:
        return handler_for_out(assets.portfolio_bonds)
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return handler_for_out(parsing_bonds_portfolio(doc))


def get_name(tiker):
    tiker_info = assets.bonds.get(tiker)
    if tiker_info is not None:
        return tiker_info[0]
    return ""


def get_income(tiker):
    tiker_info = assets.bonds.get(tiker)
    if tiker_info is not None:
        return tiker_info[2]
    return ""