import PySimpleGUI as sg
import pandas as pd

from Assets import Assets

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


def load_menu():
    ftypes = [('Документы', '*.xlsx'), ('Документы', '*.xls'), ('Все файлы', '*')]
    dlg = sg.filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    if fl != '':
        df = pd.read_excel(fl)
        return df
    return


def pars_doc_elem(doc):
    comission = 0
    my_money = 0
    dividents = 0
    tax = 0
    count = 0

    while count < len(doc['Операция']):
        if doc['Операция'][count] == 'Списание комиссии':
            comission += doc['Сумма'][count]
        if doc['Операция'][count] == 'Ввод ДС':
            my_money += doc['Сумма'][count]
        if doc['Операция'][count] == 'Вывод ДС':
            my_money -= doc['Сумма'][count]
        if doc['Операция'][count] == 'Зачисление дивидендов':
            dividents += doc['Сумма'][count]
        if doc['Операция'][count] == 'Списание налогов':
            tax += doc['Сумма'][count]
        count += 1

    comission = round(comission, 2)
    my_money = round(my_money, 2)
    dividents = round(dividents, 2)
    tax = round(tax, 2)
    write_text = 'Комисия составила:\t' + str(comission) + 'р.\n'
    write_text += 'Зачисленная сумма:\t' + str(my_money) + 'р.\n'
    write_text += 'Зачисленно дивидендов:\t' + str(dividents) + 'р.\n'
    write_text += 'Оплачено налога:\t\t' + str(tax) + 'р.\n'
    write_text += 'Итог:\t\t\t' + str(my_money - comission - tax + dividents) + 'р.\n'

    list_header = []
    list_values = []
    for element in doc.columns:
        list_header.append(element)
    for element in doc.values:
        list_data = []
        for data in element:
            list_data.append(data)
        list_values.append(list_data)

    return list_header, list_values, write_text


def pars_doc_deals(doc):
    list_header = []
    list_values = []
    filter = [0, 1, 6, 13, 17]
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
                list_data.append(element[count])
            count += 1
        list_values.append(list_data)
    return list_header, list_values


def my_stock_info(doc):
    write_text = ""

    return write_text
