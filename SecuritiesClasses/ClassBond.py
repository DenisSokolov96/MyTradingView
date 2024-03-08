from Assets import Assets

assets = Assets()


class ClassBond:
    """
        ###, Наименование, Компания, Цена сейчас,  Ср. цена, Изм. инвест. р., Количество, Инвестировано,
        Доход %, НКД общий, Продано(шт.), Продажа(р.), 1 Бонд(р.), Перевод к другому брокеру
    """
    __info_bonds = {
        'num': 0,
        'name': 'not name',  # def info_bonds
        'company': 'not name',  # def info_bonds
        'price_now': 0,  # def info_bonds
        'middle_price': 0,  # def count_money
        'change_invest': 0,  # def count_money
        'invest': 0,  # def count_money
        'count': 0,  # def add_property
        'income': 0,  # def count_money
        'nkd_now': 0,  # def add_property
        'sold_count': 0,  # def add_property
        'sold': 0,  # def add_property
        'price_sold': 0,  # def add_property
        'transfer': False
    }

    # купил/продал, цена
    __list_bonds = []

    def __init__(self):
        self.__list_bonds = ClassBond.__list_bonds.copy()
        self.__info_bonds = ClassBond.__info_bonds.copy()

    # получить список купил/продал, цена
    @property
    def list_bonds(self):
        return self.__list_bonds

    # добавить облигацию
    @list_bonds.setter
    def list_bonds(self, mas):
        count_bonds = mas[0]
        operation = mas[1]
        sum = mas[2]
        self.__list_bonds.append([count_bonds, operation, sum])

    # получить список для вывода
    @property
    def info_bonds(self):
        return self.__info_bonds

    # добавить данные в список вывода
    @info_bonds.setter
    def info_bonds(self, mas):
        name = mas[0]
        self.__info_bonds['name'] = name
        self.__info_bonds['company'] = self.get_name(name)
        self.__info_bonds['price_now'] = self.get_price(name) * 1000 / 100

    # получить название компании по тикеру
    def get_name(self, tiker):
        tiker_info = assets.bonds.get(tiker)
        if tiker_info is not None:
            return tiker_info[0]
        return ""

    # получить стоимость актива в данный момент по тикеру
    def get_price(self, tiker):
        bond_info = assets.bonds.get(tiker)
        if bond_info is not None:
            return bond_info[1]
        # если данные не найдены, то 100 так она погашена
        return 100

    # добавление данных(номер, кол-во купленных, кол-во проданных, общая и одиночная стоимость продажи) в форму вывода
    def add_property(self):
        count, sold_count, sold = self.get_count()
        self.__info_bonds['count'] = count
        self.__info_bonds['sold_count'] = sold_count
        self.__info_bonds['sold'] = sold
        self.__info_bonds['price_sold'] = round((sold / sold_count if sold > 0 else 0), 2)
        self.__info_bonds['nkd_now'] = self.get_nkd_now(self.__info_bonds['name']) * count
        self.count_money()

    # добавление данных (инивестированно, средняя цена инвестиции, изменение инвестиций)
    def count_money(self):
        count = self.__info_bonds['count']
        index = 0
        invest = 0
        for mas_bond in reversed(self.__list_bonds):
            if mas_bond[1] == "Покупка" and index < count:
                invest += mas_bond[2]
                index += 1

        if invest > 0:
            self.__info_bonds['invest'] = round(invest, 2)
            self.__info_bonds['middle_price'] = (round(invest / count, 3) if count > 0 else
                                                 round(invest / self.__info_bonds['sold_count'], 3))
        price_now = self.__info_bonds['price_now']
        self.__info_bonds['change_invest'] = self.get_dif(price_now, count, self.__info_bonds['invest'])

    # подсчет кол-ва купленных и проданных, а так же общая стоимость продажи
    def get_count(self):
        count, bond_count = 0, 0
        bond = 0.0
        for mas_bond in self.__list_bonds:
            if mas_bond[1] == "Покупка":
                count += mas_bond[0]
            if mas_bond[1] == "Продажа":
                bond_count += mas_bond[0]
                bond += mas_bond[2]
        bond = round(bond, 2)
        return count - bond_count, bond_count, bond

    def get_nkd_now(self, name):
        nkd_now = assets.bonds.get(name)
        if nkd_now is not None:
            return nkd_now[2]
        return ""

    def get_income(self, name):
        name_info = assets.bonds.get(name)
        if name_info is not None:
            return name_info[3]
        return ""

    def get_dif(self, price, count, total):
        if price is None or count == '' or total == '':
            return "-"
        else:
            return round(price * count - total, 2)
