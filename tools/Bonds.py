import Parsing
from Assets import Assets
from Binding import check_none
import api_mcx

assets = Assets()


def parsing_bonds_portfolio(doc):
    if len(assets.bonds) == 0:
        api_mcx.Handler.get_bonds()
    list_header = ['###', 'Наименование', 'Компания', 'Количество', 'Инвестировано', 'Доход %',
                   'Продано(шт.)', 'Продажа(р.)', '1 Бонд(р.)']
    list_values = []
    portfolio_bonds = {}
    for element in reversed(doc.values):
        if element[5] == 'Облигация':
            list_el = portfolio_bonds.get(element[4])
            if list_el is None:
                portfolio_bonds[element[4]] = [element[4], element[8], round(element[16], 2), 0, 0]
            else:
                if element[7] == 'Покупка':
                    portfolio_bonds[element[4]] = [element[4], element[8] + list_el[1],
                                                   round(element[16] + list_el[2], 2), list_el[3], list_el[4]]
                else:
                    portfolio_bonds[element[4]] = [element[4], list_el[1], list_el[2],
                                                    element[8] + list_el[3], round(list_el[4] + element[16], 2)]

    history_bonds = []
    for element in portfolio_bonds.values():
        if element[1] > element[3]:
            if element[3] > 0:
                element.append(round(element[4]/element[3], 2))
            else:
                element.append(0)
            list_values.append(element)
        else:
            element.append(round(element[4]/element[3], 2))
            history_bonds.append(element)

    count = 1
    for element in list_values:
        element.insert(0, count)
        element.insert(2, get_name(element[1]))
        element.insert(5, get_income(element[1]))
        count += 1

    count = 1
    for element in history_bonds:
        element.insert(0, count)
        count += 1

    assets.portfolio_bonds = [list_header, list_values]
    assets.history_bonds = check_none(history_bonds, len(list_header))
    return list_header, list_values


def get_my_bonds():
    if len(assets.portfolio_bonds[0]) > 0:
        return assets.portfolio_bonds
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return parsing_bonds_portfolio(doc)


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