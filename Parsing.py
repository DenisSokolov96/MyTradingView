from Assets import Assets
from datetime import datetime
from Binding import *

assets = Assets()


def load_data(parameter):
    if parameter == 1:
        if assets.deposits_write_offs is None:
            assets.deposits_write_offs = load_menu()
            return assets.deposits_write_offs
        else:
            return assets.deposits_write_offs
    if parameter == 0:
        if assets.doc_deals is None:
            assets.doc_deals = load_menu()
            return assets.doc_deals
        else:
            return assets.doc_deals


def write_offs(doc):
    comission = 0
    my_money = 0
    dividents = 0
    tax = 0
    coupon = 0
    count = 0
    other = 0

    while count < len(doc['Операция']):
        if doc['Операция'][count] == 'Списание комиссии':
            comission += doc['Сумма'][count]
        elif doc['Операция'][count] == 'Ввод ДС':
            my_money += doc['Сумма'][count]
        elif doc['Операция'][count] == 'Вывод ДС':
            my_money -= doc['Сумма'][count]
        elif doc['Операция'][count] == 'Зачисление дивидендов':
            dividents += doc['Сумма'][count]
        elif doc['Операция'][count] == 'Списание налогов':
            tax += doc['Сумма'][count]
        elif doc['Операция'][count] == 'Зачисление купона':
            coupon += doc['Сумма'][count]
        else:
            other += doc['Сумма'][count]
        count += 1

    comission = round(comission, 2)
    my_money = round(my_money, 2)
    dividents = round(dividents, 2)
    tax = round(tax, 2)
    coupon = round(coupon, 2)
    write_text = 'Зачисленная сумма:\t' + str(my_money) + 'р.\t'
    write_text += 'Зачисленно дивидендов:\t' + str(dividents) + 'р.\n'
    write_text += 'Комисия составила:\t' + str(comission) + 'р.\t'
    write_text += 'Доход с облигаций:\t' + str(coupon) + 'р.\n'
    write_text += 'Оплачено налога:\t\t' + str(tax) + 'р.\t'
    write_text += 'Итог:\t\t\t' + str(round(my_money - comission - tax + dividents + coupon)) + 'р.\t\t'
    write_text += 'Другие суммы: ' + str(other) + 'р.\t'

    list_header = []
    list_values = []
    filter = [0, 3, 6, 7, 9, 10, 11, 12, 13]
    count = 0
    while count < len(doc.columns):
        if count not in filter:
            list_header.append(doc.columns[count])
        count += 1

    for element in doc.values:
        list_data = []
        count = 0
        while count < len(element):
            if count not in filter:
                if count in (1, 2):
                    element[count] = datetime.strptime(str(element[count]),
                                                       '%Y-%m-%d %H:%M:%S').strftime("%H:%M %d/%m/%Y")
                list_data.append(element[count])
            count += 1
        list_values.append(list_data)

    return list_header, list_values, write_text


def pars_doc_deals(doc):
    list_header = []
    list_values = []
    filter = [0, 1, 6, 13, 17, 18, 19, 20, 21, 22]
    count = 0
    while count < len(doc.columns):
        if count not in filter:
            if doc.columns[count] == 'Код финансового инструмента':
                list_header.append('Тикер')
            elif doc.columns[count] == 'Тип финансового инструмента':
                list_header.append('Тип')
            elif doc.columns[count] == 'Сумма зачисления/списания':
                list_header.append('Сумма')
            elif doc.columns[count] == 'Комиссия торговой системы':
                list_header.append('Комисс. торг. сист.')
            else:
                list_header.append(doc.columns[count])
        count += 1

    for element in doc.values:
        list_data = []
        count = 0
        while count < len(element):
            if count not in filter:
                if count == 16:
                    element[count] = round(element[count], 2)
                if count in (2, 3):
                    element[count] = datetime.strptime(str(element[count]),
                                                       '%Y-%m-%d %H:%M:%S').strftime("%H:%M %d/%m/%Y")
                list_data.append(element[count])
            count += 1
        list_values.append(list_data)

    return list_header, list_values
