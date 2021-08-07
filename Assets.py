"""
    Pattern singleton for storing assets.
"""


class Assets:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._deposits_write_offs = None
            cls._doc_deals = None
            cls._portfolio_stocks = [[],[]]
            cls._portfolio_bonds = [[], []]
            cls._portfolio_pies = [[], []]

            # all real time
            cls._rus_stocks = {}
            cls._unrus_stocks = {}
            cls._bonds = {}
            cls._pies = {}

            # sold
            cls._history_stocks = []
            cls._history_bonds = []
            cls.history_pies = []
            cls.instance = super(Assets, cls).__new__(cls)
        return cls.instance

    @property
    def deposits_write_offs(cls):
        return cls._deposits_write_offs

    @deposits_write_offs.setter
    def deposits_write_offs(cls, _deposits_write_offs):
        cls._deposits_write_offs = _deposits_write_offs

    @property
    def doc_deals(cls):
        return cls._doc_deals

    @doc_deals.setter
    def doc_deals(cls, _doc_deals):
        cls._doc_deals = _doc_deals

    @property
    def portfolio_stocks(cls):
        return cls._portfolio_stocks[0], cls._portfolio_stocks[1]

    @portfolio_stocks.setter
    def portfolio_stocks(cls, list_portfolio):
        cls._portfolio_stocks = list_portfolio

    @property
    def rus_stocks(cls):
        return cls._rus_stocks

    @rus_stocks.setter
    def rus_stocks(cls, _rus_stocks):
        cls._rus_stocks = _rus_stocks

    @property
    def unrus_stocks(cls):
        return cls._unrus_stocks

    @unrus_stocks.setter
    def unrus_stocks(cls, _unrus_stocks):
        cls._unrus_stocks = _unrus_stocks

    @property
    def history_stocks(cls):
        return cls._history_stocks

    @history_stocks.setter
    def history_stocks(cls, _history_stocks):
        cls._history_stocks = _history_stocks

    @property
    def bonds(cls):
        return cls._bonds

    @bonds.setter
    def bonds(cls, _bonds):
        cls._bonds = _bonds

    @property
    def portfolio_bonds(cls):
        return cls._portfolio_bonds[0], cls._portfolio_bonds[1]

    @portfolio_bonds.setter
    def portfolio_bonds(cls, list_portfolio):
        cls._portfolio_bonds = list_portfolio

    @property
    def history_bonds(cls):
        return cls._history_bonds

    @history_bonds.setter
    def history_bonds(cls, _history_bonds):
        cls._history_bonds = _history_bonds

    @property
    def pies(cls):
        return cls._pies

    @pies.setter
    def pies(cls, _pies):
        cls._pies = _pies

    @property
    def portfolio_pies(cls):
        return cls._portfolio_pies[0], cls._portfolio_pies[1]

    @portfolio_pies.setter
    def portfolio_pies(cls, list_portfolio):
        cls._portfolio_pies = list_portfolio

    @property
    def history_pies(cls):
        return cls._history_pies

    @history_pies.setter
    def history_pies(cls, _history_pies):
        cls._history_pies = _history_pies
