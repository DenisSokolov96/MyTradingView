from Assets import Assets

assets = Assets()


class ClassStock:
    """
        '###', 'Компания', 'Бумага', 'Тикер', 'Цена сейчас р.', 'Ср. цена', 'Изм. инвест. р.',
        'Количество', 'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.', 'Цена за одну р.', 'Прибыль р.',
        'Страна'
    """
    __info_stocks = {
        'num': 0,  # def count_result
        'company': 'not name',  # def set_info
        'paper': 'not name',  # def set_info
        'tiker': 'not name',  # def set_info
        'price_now': 0,  # def set_info
        'middle_price': 0,  # def __count_money
        'change_invest': 0,  # def __count_money
        'count': 0,  # def count_result
        'invest': 0,  # def __count_money
        'sold_count': 0,  # def count_result
        'sold': 0,  # def count_result
        'price_sold': 0,  # def count_result
        'income': 0,  # def __count_money
        'country': 'not name'  # def set_info
    }

    # купил/продал, цена
    __list_stocks = []

    def __init__(self):
        if len(self.__list_stocks) > 0:
            self.__list_stocks = ClassStock.__list_stocks.copy()
            self.__info_stocks = ClassStock.__info_stocks.copy()

    # получить список купил/продал и цены
    @property
    def list_stock(self):
        return self.__list_stocks

    # добавить акцию
    @list_stock.setter
    def list_stock(self, mas):
        count_stocks = mas[0]
        operation = mas[1]
        sum = mas[2]
        lot_size = self.__get_lot(self.__info_stocks['tiker'])
        for i in range(0, int(count_stocks / lot_size)):
            self.__list_stocks.append([operation, round(sum / int(count_stocks / lot_size), 3)])

    # получить список для вывода
    @property
    def info_stocks(self):
        return self.__info_stocks

    # добавить данные в список вывода
    @info_stocks.setter
    def info_stocks(self, mas):
        paper = mas[0]
        country = mas[1]
        tiker = mas[2]
        self.__info_stocks['paper'] = paper
        self.__info_stocks['country'] = country
        self.__info_stocks['tiker'] = tiker
        self.__info_stocks['company'] = self.__get_name(tiker)
        self.__info_stocks['price_now'] = self.__get_price(tiker)

    # получить название компании по тикеру
    @staticmethod
    def __get_name(tiker):
        stock_info = assets.rus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[0]
        stock_info = assets.unrus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[0]
        return ""

    # получить стоимость актива в данный момент по тикеру
    @staticmethod
    def __get_price(tiker):
        stock_info = assets.rus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[2]
        stock_info = assets.unrus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[2]
        return ""

    # получить кол-во акций в лоте
    @staticmethod
    def __get_lot(tiker):
        stock_info = assets.rus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[1]
        stock_info = assets.unrus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[1]
        # если ошибка при получении значений, то возвращаю 10
        return 10
        pass

    # добавление данных(номер, кол-во купленных, кол-во проданных, общая и одиночная стоимость продажи) в форму вывода
    def count_result(self, num):
        self.__info_stocks['num'] = num
        count, sold_count, sold = self.get_count()
        self.__info_stocks['count'] = count
        self.__info_stocks['sold_count'] = sold_count
        self.__info_stocks['sold'] = sold
        lot_size = self.__get_lot(self.__info_stocks['tiker'])
        self.__info_stocks['price_sold'] = (sold / (sold_count * lot_size)
                                            if sold > 0 else 0)
        self.count_money()

    # подсчет кол-ва купленных и проданных, а так же общая стоимость продажи
    def get_count(self):
        count, sold_count = 0, 0
        sold = 0.0
        for mas_stock in self.__list_stocks:
            if mas_stock[0] == "Покупка":
                count += 1
            if mas_stock[0] == "Продажа":
                sold_count += 1
                sold += mas_stock[1]
        sold = round(sold, 3)
        return count - sold_count, sold_count, sold

    # добавление данных (инивестированно, средняя цена инвестиции, изменение инвестиций)
    def count_money(self):
        count = self.__info_stocks['count']
        index = 0
        invest = 0
        for mas_stock in reversed(self.__list_stocks):
            if mas_stock[0] == "Покупка" and index < count:
                invest += mas_stock[1]
                index += 1

        self.__info_stocks['invest'] = round(invest, 3)
        self.__info_stocks['middle_price'] = (round(invest / count, 2) if count > 0 else
                                             round(invest / self.__info_stocks['sold_count'], 2))
        lot_size = self.__get_lot(self.__info_stocks['tiker'])
        price_now = self.__info_stocks['price_now']

        self.__info_stocks['change_invest'] = (round(price_now * lot_size * count - invest, 2)
                                              if price_now is not None and price_now != "" else '-')

        ind = 1
        buy = 0
        for mas_stock in self.__list_stocks:
            if mas_stock[0] == "Покупка":
                buy += mas_stock[1]
                ind += 1
            if ind > 6:
                break
        sold = self.__info_stocks['sold']
        self.__info_stocks['income'] = (round((sold - buy) -
                                             round((sold - buy) * 0.13, 0), 2)
                                       if self.__info_stocks['sold'] > 0 else 0)
