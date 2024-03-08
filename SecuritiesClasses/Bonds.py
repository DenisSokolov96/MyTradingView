import Binding
import Parsing
import api_mcx
from Assets import Assets
from SecuritiesClasses import ClassBond

assets = Assets()


def get_my_portfolio():
    if len(assets.portfolio_bonds[0]) > 0:
        return Binding.handler_for_out(assets.portfolio_bonds, "bond")
    else:
        doc_deals = Parsing.load_data(0)
        doc_trans_security = Parsing.load_data(2)
        if doc_deals is None:
            return None, None
        return Binding.handler_for_out(start_parsing_bonds(doc_deals, doc_trans_security), "bond")


def start_parsing_bonds(doc_deals, doc_trans_security):
    if len(assets.bonds) == 0:
        api_mcx.Handler.get_bonds()
    list_header = ['###', 'Наименование', 'Компания', 'Цена сейчас р.', 'Ср. цена', 'Изм. инвест. р.',
                   'Инвестировано', 'Количество', 'Доход %', 'НКД общий', 'Продано(шт.)', 'Продажа(р.)', '1 Бонд(р.)']
    portfolio_bonds = {}
    history_bonds = {}
    for element in reversed(doc_deals.values):
        if element[5] == 'Облигация':
            if portfolio_bonds.get(element[4]) is None:
                bond = ClassBond()
                bond.info_bonds = [element[4]]
            else:
                bond = portfolio_bonds.get(element[4])
            bond.list_bonds = [element[8], element[7], round(element[16], 2)]
            portfolio_bonds[element[4]] = bond

    for bond in portfolio_bonds.values():
        bond.add_property()
        if bond.info_bonds['company'] == '':
            bond.info_bonds['transfer'] = True
            history_bonds[bond.info_bonds['name']] = bond
            continue
        if bond.info_bonds['count'] == 0:
            history_bonds[bond.info_bonds['name']] = bond

    for bond in history_bonds:
        del portfolio_bonds[bond]

    assets.portfolio_bonds = [list_header, portfolio_bonds]
    assets.history_bonds = history_bonds
    return list_header, portfolio_bonds
