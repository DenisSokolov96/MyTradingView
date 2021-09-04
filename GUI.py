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
                ['&Мой портфель', ['&Просмотреть портфель', '&Мои сделки', '&Операции по счету', '&График ввода ДС']],
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
               sg.Output(size=(65, 35), key='out', background_color='white')]]
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
        window['out'].update(redact(api_mcx.Handler.get_newtext_id(id_news)))
    ################################################
    if event == "Российские акции":
        list_data, list_columns, info = api_mcx.Handler.get_stocks_15m_ago('ru')
        wind_table(list_data, list_columns, info)
        window['out'].update("")
        return
    if event == "Зарубежные акции":
        list_data, list_columns, info = api_mcx.Handler.get_stocks_15m_ago('unru')
        wind_table(list_data, list_columns, info)
        window['out'].update("")
        return
    if event == "Облигации":
        list_data, list_columns, info = api_mcx.Handler.get_bonds()
        wind_table(list_data, list_columns, info)
        window['out'].update("")
        return
    if event == "Фонды":
        list_data, list_columns, info = api_mcx.Handler.get_pies()
        wind_table(list_data, list_columns, info)
        window['out'].update("")
        return
    ################################################
    if event == "Обновить новости":
        window['-TABLE_NEWS-'].update(api_mcx.Handler.get_list_news())
        return
    if event == "Мои сделки":
        # parametr - 0 for deals
        doc = load_data(0)
        if doc is not None:
            wind_my_deals(doc)
        window['out'].update("")
        return
    if event == "Операции по счету":
        # parametr - 1 for account transactions
        doc = load_data(1)
        if doc is not None:
            wind_my_money(doc)
        window['out'].update("")
        return
    if event == "График ввода ДС":
        create_graph()
    if event == "Просмотреть портфель":
        wind_portfolio()
    ################################################
    if event == "Автозагрузка файлов":
        wind_auto_load()


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
    layout = [[sg.Table(values=list_values, headings=list_header, def_col_width=20, max_col_width=40,
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
    list_header_stocks, list_values_stocks = tools.Stocks.get_my_portfolio()
    list_header_bonds, list_values_bonds = tools.Bonds.get_my_bonds()
    list_header_pies, list_values_pies = tools.Pie.get_my_pies()

    menu_def = [['&Общие диаграммы', ['&Круговая диаграмма', '&Столбчатая диаграмма',
                                      '&Состав портфеля по категориям']],
                ['&Акции', ['&Виды акций', '&Акции в портфеле']],
                ['&Облигации', ['&Виды облигаций']],
                ['&Фонды', ['&Состав фондов']],
                ['&Информация', ['&Проданные активы']]]

    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Table(values=list_values_stocks, headings=list_header_stocks, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=11,
                        alternating_row_color='white',
                        key='-TABLE_STOCKS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)],
              [sg.Table(values=list_values_bonds, headings=list_header_bonds, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=7,
                        alternating_row_color='white',
                        key='-TABLE_BONDS-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30),
              sg.Table(values=list_values_pies, headings=list_header_pies, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=7,
                        alternating_row_color='white',
                        key='-TABLE_PIE-',
                        selected_row_colors=('Black', 'lightgray'),
                        row_height=30)]
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
                        row_height=30),
              sg.Table(values=list_history_pies, headings=assets.portfolio_pies[0], def_col_width=20,
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
