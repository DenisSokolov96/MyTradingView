import math

import tools
import api_mcx
from Parsing import *
from XMLRefact import *
import PySimpleGUI as sg

sizeX = 1150
sizeY = 600


# основное окно
def main_wind():
    sg.theme('Light Green')
    menu_def = [['&Информация', ['&Обновить новости']],
                ['&Стоимость активов на бирже', ['&Российские акции', '&Зарубежные акции', '&Облигации', '&Фонды']],
                ['&Мой портфель', ['&Общий отчет инвестиций', '&Просмотреть портфель', '&Мои сделки',
                                   '&Операции по счету', '&График ввода ДС']],
                ['&Настройки', ['&Автозагрузка файлов']]]
    news_list = api_mcx.Handler.get_list_news()
    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Table(values=news_list, headings=['Дата', 'Новость'], def_col_width=12, max_col_width=60,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='left',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_NEWS-',
                        selected_row_colors=('Black', 'lightgray'),
                        enable_events=True,
                        row_height=30),
               sg.Frame('', [
                   [sg.Input(size=(60, 1), key='out_price', readonly=True, justification='center',
                             default_text=api_mcx.Handler.get_securities_rates(),
                             disabled_readonly_background_color='lightblue')],
                   [sg.Output(size=(60, 35), key='out', background_color='white')]
               ]
                        )
               ]
              ]
    window = sg.Window('Мои инвестиции', layout, size=(sizeX, sizeY))
    while True:
        event, values = window.read()
        func_menu(event, window, values, news_list)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()


def func_menu(event, window, values, news_list):
    window['out_price'].update(api_mcx.Handler.get_securities_rates())
    window['out'].update("")
    if event == '-TABLE_NEWS-':
        id_news = news_list[values['-TABLE_NEWS-'][0]][2]
        window['out'].update(redact(api_mcx.Handler.get_newtext_id(id_news)))
    ################################################
    if event == "Российские акции":
        list_data, list_columns, info = api_mcx.Handler.get_stocks_15m_ago('ru')
        wind_table(list_data, list_columns, info)
        return
    if event == "Зарубежные акции":
        list_data, list_columns, info = api_mcx.Handler.get_stocks_15m_ago('unru')
        wind_table(list_data, list_columns, info)
        return
    if event == "Облигации":
        list_data, list_columns, info = api_mcx.Handler.get_bonds()
        wind_table(list_data, list_columns, info)
        return
    if event == "Фонды":
        list_data, list_columns, info = api_mcx.Handler.get_pies()
        wind_table(list_data, list_columns, info)
        return
    ################################################
    if event == "Обновить новости":
        window['-TABLE_NEWS-'].update(api_mcx.Handler.get_list_news())
        return
    ################################################
    if event == "Мои сделки":
        # parametr - 0 for deals
        doc = load_data(0)
        if doc is not None:
            wind_my_deals(doc)
        return
    if event == "Операции по счету":
        # parametr - 1 for account transactions
        doc = load_data(1)
        if doc is not None:
            wind_my_money(doc)
        return
    if event == "График ввода ДС":
        create_graph()
    if event == "Просмотреть портфель":
        wind_portfolio()
    if event == "Общий отчет инвестиций":
        wind_report_invest()
    ################################################
    if event == "Автозагрузка файлов":
        wind_auto_load()


# вывод данных с биржи
def wind_table(list_data, list_columns, info):
    page_count = math.ceil(len(list_data) / 12)
    index_page = 1
    layout = [
        [sg.Combo(values=[], enable_events=True, key='-search-', size=(35, 1)),
         sg.Button(button_text='Вперед', key='-forward-'), sg.Button(button_text='Назад', key='-back-'),
         sg.Input(default_text="1 из " + str(page_count), key='-out-',
                  readonly=True, text_color='Black', size=(10, 1), justification='center')],
        [sg.Table(values=list_data[:12], headings=list_columns, def_col_width=20, max_col_width=50,
                  background_color='lightblue', text_color='Black', auto_size_columns=True,
                  justification='centre', num_rows=12, alternating_row_color='white',
                  key='-TABLE_RU-', enable_events=True, selected_row_colors=('Black', 'lightgray'), row_height=30,
                  tooltip=info)],
    [sg.Text('*Нажатие на строку с ценной бумагой отразит дивидендную доходность\n и историю изменения цены',
             background_color="lightblue")]]
    sg.theme('BlueMono')
    new_win = sg.Window(info, layout, return_keyboard_events=True)
    while True:
        event, values = new_win.read()

        if event == '-TABLE_RU-':
            index = (index_page - 1) * 12 + (values['-TABLE_RU-'][0])
            tiker = list_data[index][1]
            if info == "Российские акции":
                wind_dividends(api_mcx.Handler.get_dividends(tiker), tiker, list_data[index][0])
            if info == "Облигации":
                wind_nkd(api_mcx.Handler.get_nkd(list_data[index][0]), tiker)
        if event == '-back-' and index_page < page_count:
            index_page += 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_RU-'].update(list_data[(index_page - 1) * 12:index_page * 12])
        if event == '-forward-' and index_page > 1:
            index_page -= 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_RU-'].update(list_data[(index_page - 1) * 12:index_page * 12])
        if event == '\r':
            list_dates = search(list_data, values['-search-'], info)
            new_win['-search-'].update(values=list_dates)
            new_win['-search-'].Widget.event_generate('<Down>')
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Операции по счету
def wind_my_money(doc):
    list_header, list_values, write_text = write_offs(doc)
    page_count = math.ceil(len(list_values) / 15)
    index_page = 1
    layout = [[sg.Text(size=(70, 3), key='out', text=write_text)],
              [sg.Table(values=list_values[:15], headings=list_header, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=15,
                        alternating_row_color='white',
                        key='-TABLE_MONEY-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)],
              [sg.Button(button_text='Вперед', key='-forward-'), sg.Button(button_text='Назад', key='-back-'),
               sg.Input(default_text="1 из " + str(page_count), key='-out-',
                        readonly=True, text_color='Black', size=(10, 1), justification='center')]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Операции по счету', layout)
    while True:
        event, values = new_win.read()
        if event == '-back-' and index_page < page_count:
            index_page += 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_MONEY-'].update(list_values[(index_page - 1) * 15:index_page * 15])
        if event == '-forward-' and index_page > 1:
            index_page -= 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_MONEY-'].update(list_values[(index_page - 1) * 15:index_page * 15])
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Мои сделки
def wind_my_deals(doc):
    list_header, list_values = pars_doc_deals(doc)
    page_count = math.ceil(len(list_values) / 15)
    index_page = 1
    layout = [
        [sg.Table(values=list_values[:15], headings=list_header, def_col_width=15,
                  background_color='lightblue',
                  text_color='Black',
                  auto_size_columns=True,
                  justification='centre',
                  num_rows=15,
                  alternating_row_color='white',
                  key='-TABLE_DEALS-',
                  selected_row_colors=('Black', 'lightgray'),
                  row_height=30)],
        [sg.Button(button_text='Вперед', key='-forward-'), sg.Button(button_text='Назад', key='-back-'),
         sg.Input(default_text="1 из " + str(page_count), key='-out-',
                  readonly=True, text_color='Black', size=(10, 1), justification='center')]
    ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои сделки', layout)
    while True:
        event, values = new_win.read()
        if event == '-back-' and index_page < page_count:
            index_page += 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_DEALS-'].update(list_values[(index_page - 1) * 15:index_page * 15])
        if event == '-forward-' and index_page > 1:
            index_page -= 1
            new_win['-out-'].update(str(index_page) + ' из ' + str(page_count))
            new_win['-TABLE_DEALS-'].update(list_values[(index_page - 1) * 15:index_page * 15])
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# просмотр портфеля
def wind_portfolio():
    list_header_stocks, list_values_stocks = tools.Stocks.get_my_portfolio()
    list_header_bonds, list_values_bonds = tools.Bonds.get_my_bonds()
    list_header_pies, list_values_pies = tools.Pie.get_my_pies()

    list_colors_stocks = []
    for i in range(0, len(list_values_stocks)):
        if list_values_stocks[i][6] > 0:
            list_colors_stocks.append([i, "green", "lightblue" if i % 2 else "white"])
    list_colors_bonds = []
    for i in range(0, len(list_values_bonds)):
        if list_values_bonds[i][5] > 0:
            list_colors_bonds.append([i, "green", "lightblue" if i % 2 else "white"])
    list_colors_pies = []
    for i in range(0, len(list_values_pies)):
        if list_values_pies[i][4] > 0:
            list_colors_pies.append([i, "green", "lightblue" if i % 2 else "white"])

    menu_def = [['&Общие диаграммы', ['&Круговая диаграмма', '&Столбчатая диаграмма',
                                      '&Состав портфеля по категориям']],
                ['&Акции', ['&Виды акций', '&Акции в портфеле']],
                ['&Облигации', ['&Виды облигаций']],
                ['&Фонды', ['&Состав фондов']],
                ['&Информация', ['&Проданные активы']]]

    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Table(values=list_values_stocks, headings=list_header_stocks, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black', row_colors=list_colors_stocks,
                        auto_size_columns=True, justification='centre', num_rows=7, alternating_row_color='white',
                        key='-TABLE_STOCKS-', selected_row_colors=('Black', 'lightgray'), row_height=30)],
              [sg.Table(values=list_values_bonds, headings=list_header_bonds, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black', row_colors=list_colors_bonds,
                        auto_size_columns=True, justification='centre', num_rows=5, alternating_row_color='white',
                        key='-TABLE_BONDS-', selected_row_colors=('Black', 'lightgray'), row_height=30)],
              [sg.Table(values=list_values_pies, headings=list_header_pies, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black', row_colors=list_colors_pies,
                        auto_size_columns=True, justification='centre', num_rows=5, alternating_row_color='white',
                        key='-TABLE_PIE-', selected_row_colors=('Black', 'lightgray'), row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои данные', layout)
    while True:
        event, values = new_win.read()
        if event == 'Круговая диаграмма':
            get_diagramma_circle()
        if event == 'Столбчатая диаграмма':
            get_diagramma_column()
        if event == 'Проданные активы':
            wind_history()
        if event == 'Состав портфеля по категориям':
            get_diagramma_compos()
        if event == 'Виды акций':
            get_rus_unrus_stocks()
        if event == 'Состав фондов':
            get_all_pies()
        if event == 'Виды облигаций':
            get_all_bonds()
        if event == 'Акции в портфеле':
            get_name_stocks()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# просмотр исторического портфеля
def wind_history():
    list_history_stocks = to_list(assets.history_stocks)
    list_history_bonds = to_list(assets.history_bonds)
    list_history_pies = to_list(assets.history_pies)
    layout = [[sg.Table(values=list_history_stocks, headings=assets.portfolio_stocks[0], def_col_width=20,
                        max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=5,
                        alternating_row_color='white',
                        key='-TABLE_DEALS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)],
              [sg.Table(values=list_history_bonds, headings=assets.portfolio_bonds[0],
                        def_col_width=20,
                        max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=5,
                        alternating_row_color='white',
                        key='-TABLE_BONDS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)],
              [sg.Table(values=list_history_pies, headings=assets.portfolio_pies[0], def_col_width=20,
                        max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=5,
                        alternating_row_color='white',
                        key='-TABLE_PIES-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Проданные активы', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Окно вывода общей таблицы инвестиций
def wind_report_invest():
    list_headers, list_data, list_colors = report_invest()
    layout = [[sg.Table(values=list_data, headings=list_headers, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black', row_colors=list_colors,
                        auto_size_columns=True, justification='centre', num_rows=5, alternating_row_color='white',
                        key='-TABLE_INVEST-', selected_row_colors=('Black', 'lightgray'), row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Общий отчет инвестиций', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Окно с выводом дивидендов по выбранной акции (за 100 последних дней)
def wind_dividends(list_dividends, tiker, company):
    list_headers = ['Сумма на акцию', 'Дата', 'Валюта']
    list_colors = []
    for i in range(0, len(list_dividends)):
        if list_dividends[i][0] != "" and datetime.now() < datetime.strptime(list_dividends[i][1], '%Y-%m-%d'):
            list_colors.append([i, "green", "lightblue" if i % 2 else "white"])
        if list_dividends[i][0] != "":
            list_dividends[i][1] = datetime.strptime(list_dividends[i][1], '%Y-%m-%d').strftime('%d/%m/%Y')
    menu_def = [['&Информация', ['&Показать историю цены']]]

    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Table(values=list_dividends, headings=list_headers, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black', row_colors=list_colors,
                        auto_size_columns=True, justification='centre', num_rows=10, alternating_row_color='white',
                        key='-TABLE_DIVIDENDS-', selected_row_colors=('Black', 'lightgray'), row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Дивиденды ' + tiker, layout)
    while True:
        event, values = new_win.read()
        if event == 'Показать историю цены':
            list_data_hist, list_price = api_mcx.Handler.get_history_stocks(tiker)
            create_history_graph(list_data_hist, list_price, company)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Окно с выводом нкд по облигации
def wind_nkd(list, tiker):
    list_headers = ['НКД на сегодня', 'Дата следующей выплаты', 'НКД на дату выплаты']

    layout = [[sg.Table(values=list, headings=list_headers, def_col_width=20, max_col_width=40,
                        background_color='lightblue', text_color='Black',
                        auto_size_columns=True, justification='centre', num_rows=10, alternating_row_color='white',
                        key='-TABLE_NKD-', selected_row_colors=('Black', 'lightgray'), row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('НКД ' + tiker, layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    new_win.close()


# Окно с настройками
def wind_auto_load():
    sg.theme('Light Green')
    layout = [
        [sg.Button("Сделки"), sg.Input(key='-Deal-', size=(45, 1), justification='center')],
        [sg.Button("Зач./Спис."), sg.Input(key='-Transaction-', size=(45, 1), justification='center')],
        [sg.Button("Сохранить")]
    ]
    window = sg.Window('Автозагрузка файлов', layout, size=(400, 100))
    while True:
        event, values = window.read()
        if event == 'Сделки':
            window['-Deal-'].update(set_path('сделкам'))
        if event == 'Зач./Спис.':
            window['-Transaction-'].update(set_path('эачислению/списанию'))
        if event == 'Сохранить':
            write_to_xml(values['-Deal-'], values['-Transaction-'])
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()


# Вывод окна при отсутствии интернета
def wind_error():
    sg.theme('Light Green')
    menu_def = [['&Меню', ['&Мои сделки', '&Операции по счету']]]

    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Text("Нет поключения к интернету")]]
    window = sg.Window('Мои инвестиции', layout, size=(400, 100))
    while True:
        event, values = window.read()
        func_menu(event, window, values, None)
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()
