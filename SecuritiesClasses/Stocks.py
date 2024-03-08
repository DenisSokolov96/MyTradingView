import Binding
import Parsing
import api_mcx
from Assets import Assets
from SecuritiesClasses import ClassStock

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_stocks[0]) > 0:
        return Binding.handler_for_out(assets.portfolio_stocks, "stock")
    else:
        doc_deals = Parsing.load_data(0)
        doc_trans_security = Parsing.load_data(2)
        if doc_deals is None:
            return None, None
        return Binding.handler_for_out(start_parsing_stocks(doc_deals, doc_trans_security), "stock")


def start_parsing_stocks(doc_deals, doc_trans_security):
    if len(assets.rus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('ru')
    if len(assets.unrus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('unru')

    list_header = ['###', 'Компания', 'Бумага', 'Тикер', 'Цена сейчас р.', 'Ср. цена',
                   'Изм. инвест. р.', 'Кол - во', 'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.',
                   'Цена за одну р.', 'Прибыль р.', 'Страна']
    portfolio_stocks = {}
    history_stocks = {}
    for element in reversed(doc_deals.values):
        if element[5] == 'Акция' or element[5] == 'Депозитарная расписка':
            ticket = element[4]
            if ticket in assets.old_to_new_tiket.keys():
                ticket = assets.old_to_new_tiket[ticket]
            if portfolio_stocks.get(ticket) is None:
                stock = ClassStock()
                if element[5] == 'Депозитарная расписка':
                    paper = 'Деп. рас.'
                    country = 'Др. стр.'
                else:
                    paper = 'Акция'
                    if ticket.find('-RM') != -1:
                        country = 'США'
                    else:
                        country = 'Рос.'
                stock.info_stocks = [paper, country, ticket]
            else:
                stock = portfolio_stocks.get(ticket)
            stock.list_stocks = [element[8], element[7], element[16]]
            portfolio_stocks[ticket] = stock

    for element in reversed(doc_trans_security.values):
        if element[4].find("пай") == -1 and element[4].find("блигаци") == -1:
            portfolio_stocks[element[3]].info_stocks['transfer'] = True

    for stock in portfolio_stocks.values():
        stock.add_property()
        if stock.info_stocks['transfer'] is True:
            history_stocks[stock.info_stocks['tiker']] = stock
            continue
        if stock.info_stocks['count'] == 0:
            history_stocks[stock.info_stocks['tiker']] = stock

    for stock in history_stocks:
        del portfolio_stocks[stock]

    assets.portfolio_stocks = [list_header, portfolio_stocks]
    assets.history_stocks = history_stocks
    return list_header, portfolio_stocks
