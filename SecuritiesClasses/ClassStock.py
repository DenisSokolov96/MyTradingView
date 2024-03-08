from Assets import Assets

assets = Assets()


class ClassStock:
    """
        '###', 'Компания', 'Бумага', 'Тикер', 'Цена сейчас р.', 'Ср. цена', 'Изм. инвест. р.',
        'Количество', 'Инвестировано р.', 'Продано(шт.)', 'Цена продажи р.', 'Цена за одну р.', 'Прибыль р.',
        'Страна', 'Перевод к другому брокеру'
    """
    __info_stocks = {
        'num': 0,
        'company': 'not name',  # def info_stocks
        'paper': 'not name',  # def info_stocks
        'tiker': 'not name',  # def info_stocks
        'price_now': 0,  # def info_stocks
        'middle_price': 0,  # def count_money
        'change_invest': 0,  # def count_money
        'count': 0,  # def add_property
        'invest': 0,  # def count_money
        'sold_count': 0,  # def add_property
        'sold': 0,  # def add_property
        'price_sold': 0,  # def add_property
        'income': 0,  # def count_money
        'country': 'not name',  # def info_stocks
        'transfer': False
    }

    # купил/продал, цена
    __list_stocks = []

    def __init__(self):
        self.__list_stocks = ClassStock.__list_stocks.copy()
        self.__info_stocks = ClassStock.__info_stocks.copy()

    # получить список купил/продал и цены
    @property
    def list_stocks(self):
        return self.__list_stocks

    # добавить акцию
    @list_stocks.setter
    def list_stocks(self, mas):
        count_stocks = mas[0]
        operation = mas[1]
        sum = mas[2]
        lot_size = self.__get_lot(self.__info_stocks['tiker'])
        for i in range(0, int(count_stocks / lot_size)):
            self.__list_stocks.append([count_stocks, operation, round(sum / int(count_stocks / lot_size), 3)])

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
        self.__info_stocks['company'] = self.get_name(tiker)
        self.__info_stocks['price_now'] = self.get_price(tiker)

    # получить название компании по тикеру
    def get_name(self, tiker):
        stock_info = assets.rus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[0]
        stock_info = assets.unrus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[0]
        return ""

    # получить стоимость актива в данный момент по тикеру
    def get_price(self, tiker):
        stock_info = assets.rus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[2]
        stock_info = assets.unrus_stocks.get(tiker)
        if stock_info is not None:
            return stock_info[2]
        return ""

    # получить кол-во акций в лоте
    def __get_lot(self, tiker):
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
    def add_property(self):
        count, sold_count, sold = self.get_count()
        lot_size = self.__get_lot(self.__info_stocks['tiker'])
        self.__info_stocks['count'] = count * lot_size
        self.__info_stocks['sold_count'] = sold_count * lot_size
        self.__info_stocks['sold'] = sold * lot_size
        self.__info_stocks['price_sold'] = (round(sold / sold_count, 2)
                                            if sold > 0 else 0)
        self.count_money()

    # подсчет кол-ва купленных и проданных, а так же общая стоимость продажи
    def get_count(self):
        count, sold_count = 0, 0
        sold = 0.0
        for mas_stock in self.__list_stocks:
            if mas_stock[1] == "Покупка":
                count += 1  # mas_stock[0]
            if mas_stock[1] == "Продажа":
                sold_count += 1  # mas_stock[0]
                sold += mas_stock[2]
        sold = round(sold, 3)
        return count - sold_count, sold_count, sold

    # TODO новая функция (не работает), замена def count_money
    # TODO считаю тут:
    #  self.__info_stocks['income'] - прибыль
    #  self.__info_stocks['invest'] - инивестированно
    #  self.__info_stocks['change_invest'] - изменение инвестиций
    #  self.__info_stocks['middle_price']
    #  кол-во / операция / цена
    def count_money_new(self):
        count, invest_sum, middle_price = 0, 0, 0
        count_sold, sold_sum = 0, 0
        for mas_stock in self.__list_stocks:
            if mas_stock[1] == 'Покупка':
                count += mas_stock[0]
                invest_sum += mas_stock[2] * mas_stock[0]
                middle_price = round(invest_sum / count, 2)
            if mas_stock[1] == 'Продажа':
                count_sold += mas_stock[0]
                sold_sum += mas_stock[2] * mas_stock[0]
                count -= mas_stock[0]
                invest_sum -= middle_price * mas_stock[0]
        self.__info_stocks['invest'] = round(invest_sum, 2)
        self.__info_stocks['middle_price'] = middle_price
        price_now = self.__info_stocks['price_now']
        self.__info_stocks['change_invest'] = (round(price_now * count - invest_sum, 2)
                                               if price_now is not None and price_now != "" else '-')
        #self.__info_stocks['income'] = 0



    def count_money(self):
        count = self.__info_stocks['count']
        index = 0
        invest = 0
        for mas_stock in reversed(self.__list_stocks):
            if mas_stock[1] == 'Покупка' and index < count:
                invest += mas_stock[2]
                index += 1

        if invest > 0:
            self.__info_stocks['invest'] = round(invest, 2)
            self.__info_stocks['middle_price'] = (round(invest / count, 2) if count > 0 else
                                                  round(invest / self.__info_stocks['sold_count'], 2))
        price_now = self.__info_stocks['price_now']

        self.__info_stocks['change_invest'] = (round(price_now * count - invest, 2)
                                               if price_now is not None and price_now != "" else '-')

        ind = 1
        buy = 0
        sold_count = self.__info_stocks['sold_count']
        for mas_stock in self.__list_stocks:
            if mas_stock[1] == "Покупка":
                buy += mas_stock[2]
                ind += 1
            if ind > sold_count:
                break
        sold = self.__info_stocks['sold']
        self.__info_stocks['income'] = (round((sold - buy) - round((sold - buy) * 0.13, 2), 2)
                                        if sold > 0 else 0)
