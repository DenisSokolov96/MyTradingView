import Parsing
from Assets import Assets
from Binding import check_none
import api_mcx

assets = Assets()


def parsing_pies_portfolio(doc):
    if len(assets.pies) == 0:
        api_mcx.Handler.get_pies()
    list_header = ['###', 'Наименование', 'Количество', 'Инвестировано',
                   'Продано(шт.)', 'Продажа(р.)', '1 Пай(р.)']
    list_values = []
    portfolio_pies = {}
    for element in reversed(doc.values):
        if element[5] == 'Пай':
            list_el = portfolio_pies.get(element[4])
            if list_el is None:
                portfolio_pies[element[4]] = [element[4], element[8], round(element[16], 2), 0, 0]
            else:
                if element[7] == 'Покупка':
                    portfolio_pies[element[4]] = [element[4], element[8] + list_el[1],
                                                  round(element[16] + list_el[2], 2), list_el[3], list_el[4]]
                else:
                    portfolio_pies[element[4]] = [element[4], list_el[1], list_el[2],
                                                  element[8] + list_el[3], round(list_el[4] + element[16], 2)]

    history_pies = []
    for element in portfolio_pies.values():
        if element[1] > element[3]:
            if element[3] > 0:
                element.append(round(element[4] / element[3], 2))
            else:
                element.append(0)
            list_values.append(element)
        else:
            element.append(round(element[4] / element[3], 2))
            history_pies.append(element)

    count = 1
    for element in list_values:
        element.insert(0, count)
        count += 1

    count = 1
    for element in history_pies:
        element.insert(0, count)
        count += 1

    assets.portfolio_pies = [list_header, list_values]
    assets.history_pies = check_none(history_pies, len(list_header))

    return list_header, list_values


def get_my_pies():
    if len(assets.portfolio_pies[0]) > 0:
        return assets.portfolio_pies
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return parsing_pies_portfolio(doc)


def get_name(tiker):
    tiker_info = assets.pies.get(tiker)
    if tiker_info is not None:
        return tiker_info[0]
    return ""

