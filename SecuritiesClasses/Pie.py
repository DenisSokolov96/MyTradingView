import Binding
import Parsing
import api_mcx
from Assets import Assets
from SecuritiesClasses import ClassPie

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_pies[0]) > 0:
        return Binding.handler_for_out(assets.portfolio_pies, "pie")
    else:
        doc_deals = Parsing.load_data(0)
        doc_trans_security = Parsing.load_data(2)
        if doc_deals is None:
            return None, None
        return Binding.handler_for_out(start_parsing_pies(doc_deals, doc_trans_security), "pie")


def start_parsing_pies(doc_deals, doc_trans_security):
    if len(assets.pies) == 0:
        api_mcx.Handler.get_pies()
    list_header = ['###', 'Наименование', 'Цена сейчас р.', 'Ср. цена', 'Изм. инвест. р.,', 'Инвестировано',
                   'Количество', 'Продано(шт.)', 'Продажа(р.)', '1 Пай(р.)', 'Фонд']
    portfolio_pies = {}
    history_pies = {}
    for element in reversed(doc_deals.values):
        if element[5] == 'Пай':
            ticket = element[4]
            if ticket in assets.old_to_new_tiket.keys():
                ticket = assets.old_to_new_tiket[ticket]
            if portfolio_pies.get(ticket) is None:
                pie = ClassPie()
                pie.info_pies = [ticket]
            else:
                pie = portfolio_pies.get(ticket)
            pie.list_pies = [element[8], element[7], round(element[16], 2)]
            portfolio_pies[ticket] = pie

    for element in reversed(doc_trans_security.values):
        if element[4].find("пай") != -1:
            portfolio_pies[element[3]].info_pies['transfer'] = True

    for pie in portfolio_pies.values():
        pie.add_property()
        if pie.info_pies['transfer'] is True:
            history_pies[pie.info_pies['name']] = pie
            continue
        if pie.info_pies['count'] == 0:
            history_pies[pie.info_pies['name']] = pie

    for pie in history_pies:
        del portfolio_pies[pie]

    assets.portfolio_pies = [list_header, portfolio_pies]
    assets.history_pies = history_pies
    return list_header, portfolio_pies
