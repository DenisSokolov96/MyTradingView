from Assets import Assets

assets = Assets()


class ClassPie:
    """
        ###, Наименование, Цена сейчас р., Ср. цена, Инвестировано, Изм. инвест. р.,
        Количество, Продано(шт.), Продажа(р.), 1 Пай(р.), Название фондаб , Перевод к другому брокеру
    """
    __info_pies = {
        'num': 0,
        'name': 'not name',  # def info_pies
        'price_now': 0,  # def info_pies
        'middle_price': 0,   # def get_dif
        'change_invest': 0,  # def get_dif
        'invest': 0,  # def get_dif
        'count': 0,  # def add_property
        'sold_count': 0,  # def add_property
        'sold': 0,  # def add_property
        'price_sold': 0,  # def add_property
        'name_fond': 0,  # def info_pies
        'transfer': False
    }

    # купил/продал, цена
    __list_pies = []

    def __init__(self):
        self.__list_pies = ClassPie.__list_pies.copy()
        self.__info_pies = ClassPie.__info_pies.copy()

    # получить список купил/продал и цены
    @property
    def list_pies(self):
        return self.__list_pies

    # добавить пай фонда
    @list_pies.setter
    def list_pies(self, mas):
        count_pies = mas[0]
        operation = mas[1]
        sum = mas[2]
        self.__list_pies.append([count_pies, operation, sum])

    # получить список для вывода
    @property
    def info_pies(self):
        return self.__info_pies

    # добавить данные в список вывода
    @info_pies.setter
    def info_pies(self, mas):
        name = mas[0]
        self.__info_pies['name'] = name
        self.__info_pies['name_fond'] = self.get_name(name)
        self.__info_pies['price_now'] = self.get_price(name)

    # получить стоимость актива в данный момент по названию
    def get_price(self, name):
        price = assets.pies.get(name)
        if price is not None:
            return price[0]
        return 0

    # добавление данных( кол-во купленных, кол-во проданных, общая и одиночная стоимость продажи) в форму вывода
    def add_property(self):
        count, sold_count, sold = self.get_count()
        self.__info_pies['count'] = count
        self.__info_pies['sold_count'] = sold_count
        self.__info_pies['sold'] = sold
        self.__info_pies['price_sold'] = round((sold / sold_count if sold > 0 else 0), 2)
        self.count_money()

    # подсчет кол-ва купленных и проданных, а так же общая стоимость продажи
    def get_count(self):
        count, sold_count = 0, 0
        sold = 0.0
        for mas_pie in self.__list_pies:
            if mas_pie[1] == "Покупка":
                count += mas_pie[0]
            if mas_pie[1] == "Продажа":
                sold_count += mas_pie[0]
                sold += mas_pie[2]
        sold = round(sold, 2)
        return count - sold_count, sold_count, sold

    # добавление данных (инивестированно, средняя цена инвестиции, изменение инвестиций)
    def count_money(self):
        count = self.__info_pies['count']
        index = 0
        invest = 0
        for mas_pie in reversed(self.__list_pies):
            if mas_pie[1] == "Покупка" and index < count:
                invest += mas_pie[2]
                index += 1

        if invest > 0:
            self.__info_pies['invest'] = round(invest, 2)
            self.__info_pies['middle_price'] = (round(invest / count, 3) if count > 0 else
                                                 round(invest / self.__info_pies['sold_count'], 3))
        price_now = self.__info_pies['price_now']
        self.__info_pies['change_invest'] = self.get_dif(price_now, count, self.__info_pies['invest'])

    def get_dif(self, price, count, total):
        if price is None or count == '' or total == '':
            return "-"
        else:
            return round(price * count - total, 2)

    def get_name(self, tiker):
        tiker_info = assets.pies.get(tiker)
        if tiker_info is not None:
            return tiker_info[0]
        return ""