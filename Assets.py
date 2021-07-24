"""
    Pattern singleton for storing assets.
"""


class Assets:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls._deposits_write_offs = None
            cls._doc_deals = None
            cls._portfolio = [[],[]]
            cls._rus_stocks = []
            cls._unrus_stocks = []
            cls._history_stocks = []
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
    def portfolio(cls):
        return cls._portfolio[0], cls._portfolio[1]

    @portfolio.setter
    def portfolio(cls, list_portfolio):
        cls._portfolio = list_portfolio

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