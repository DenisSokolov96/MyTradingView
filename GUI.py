from Parsing import *

sizeX = 1150
sizeY = 600


# основное окно
def main_wind():
    sg.theme('Light Green')
    menu_def = [['&Меню', ['&Обновить новости']],
                ['&Информация на бирже', ['&Российские акции', '&Зарубежные акции']],
                ['&Мой портфель', ['&Просмотреть портфель', '&Мои сделки', '&Операции по счету', '&График ввода ДС']]]
    news_list = get_list_news()
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
               sg.Output(size=(65, 35), key='out', background_color='lightgray')]]
    window = sg.Window('Мои инвестиции', layout, size=(sizeX, sizeY))

    while True:
        event, values = window.read()

        func_menu(event, window, values, news_list)

        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()


def func_menu(event, window, values, news_list):
    if event == '-TABLE_NEWS-':
        id_news = news_list[values['-TABLE_NEWS-'][0]][2]
        window['out'].update(get_newtext_id(id_news))
    ################################################
    if event == "Российские акции":
        list_data, list_columns, info = get_ru()
        wind_table(list_data, list_columns, info)
        return
    if event == "Зарубежные акции":
        list_data, list_columns, info = get_unru()
        wind_table(list_data, list_columns, info)
        return
    ################################################
    if event == "Обновить новости":
        window['-TABLE_NEWS-'].update(get_list_news())
        return
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


# вывод данных с биржи
def wind_table(list_data, list_columns, info):
    layout = [[sg.Table(values=list_data, headings=list_columns, def_col_width=20, max_col_width=50,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_RU-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30,
                        tooltip=info)]]
    sg.theme('BlueMono')
    new_win = sg.Window(info, layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


# Операции по счету
def wind_my_money(doc):
    list_header, list_values, write_text = write_offs(doc)
    layout = [[sg.Text(size=(40, 5), key='out', text=write_text)],
              [sg.Table(values=list_values, headings=list_header, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_MONEY-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Операции по счету', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


# Мои сделки
def wind_my_deals(doc):
    list_header, list_values = pars_doc_deals(doc)
    write_text = my_stock_info(doc)
    layout = [[sg.Text(size=(40, 15), key='out', text=write_text)],
              [sg.Table(values=list_values, headings=list_header, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_DEALS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои сделки', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


# просмотр портфеля
def wind_portfolio():
    list_header, list_values = get_my_portfolio()
    if list_header is None:
        return

    layout = [[sg.Button("Круговая диаграмма", button_color=("Black", "lightblue"), size=(20, 1), key='bt_diag_cir'),
              sg.Button("Столбчатая диаграмма", button_color=("Black", "lightblue"), size=(20, 1),
                         key='bt_diag_column'),
               sg.Button("Проданные активы", button_color=("Black", "lightblue"), size=(20, 1),
                         key='bt_sal_stocks')
               ],
              [sg.Table(values=list_values, headings=list_header, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_DEALS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои данные', layout)
    while True:
        event, values = new_win.read()
        if event == 'bt_diag_cir':
            get_diagramma_circle()
        if event == 'bt_diag_column':
            get_diagramma_column()
        if event == 'bt_sal_stocks':
            wind_history()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


# просмотр исторического портфеля
def wind_history():
    layout = [[sg.Table(values=assets.history_stocks, headings=assets.portfolio[0], def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='white',
                        key='-TABLE_DEALS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои данные', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


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
