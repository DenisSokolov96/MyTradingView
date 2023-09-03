import Parsing
import api_mcx
import tools
from Assets import Assets
from Binding import check_none, handler_for_out, handler_for_out_STOCKS
from Classes import ClassStock

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_stocks[0]) > 0:
        return handler_for_out_STOCKS(assets.portfolio_stocks)
    else:
        doc = Parsing.load_data(0)
        if doc is None:
            return None, None
        return handler_for_out_STOCKS(parsing_for_portfolio(doc))


def parsing_for_portfolio(doc):
    if len(assets.rus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('ru')
    if len(assets.unrus_stocks) == 0:
        api_mcx.Handler.get_stocks_15m_ago('unru')

    list_header = ['###', 'Компания', 'Бумага', 'Тикер', 'Цена сейчас р.', 'Ср. цена',
                   'Изм. инвест. р.', 'Кол - во', 'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.',
                   'Цена за одну р.', 'Прибыль р.', 'Страна']
    portfolio_stocks = {}
    history_stocks = {}
    for element in reversed(doc.values):
        if element[5] == 'Акция' or element[5] == 'Депозитарная расписка':
            if portfolio_stocks.get(element[4]) is None:
                stock = ClassStock()
                if element[5] == 'Депозитарная расписка':
                    paper = 'Деп. рас.'
                    country = 'Др. стр.'
                else:
                    paper = 'Акция'
                    if element[4].find('-RM') != -1:
                        country = 'США'
                    else:
                        country = 'Рос.'
                stock.info_stocks = [paper, country, element[4]]
            else:
                stock = portfolio_stocks.get(element[4])
            stock.list_stock = [element[8], element[7], element[16]]
            portfolio_stocks[element[4]] = stock

    num = 1
    for stock in portfolio_stocks.values():
        stock.count_result(num)
        if stock.info_stocks['count'] <= stock.info_stocks['sold_count']:
            history_stocks[stock.info_stocks['tiker']] = stock
        num += 1

    for stock in history_stocks:
        #tiker = stock.info_stocks()['tiker']
        del portfolio_stocks[stock]

    assets.portfolio_stocks = [list_header, portfolio_stocks]
    assets.history_stocks = check_none(history_stocks, len(list_header))
    return list_header, portfolio_stocks

