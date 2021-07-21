import PySimpleGUI as sg

from Handler import *
from Parsing import load_deposits_write_offs, pars_doc_elem, load_deals, pars_doc_deals, my_stock_info

sizeX = 960
sizeY = 540


def main_wind():
    sg.theme('Light Green')
    menu_def = [['&Меню', ['&Новости', '&Мои активы', '&Операции по счету']],
                ['&Информация на бирже', ['&Российские акции', '&Зарубежные акции']]]
    layout = [[sg.Output(size=(130, 35), key='out')],
              [sg.Menu(menu_def, tearoff=False)]
              ]
    window = sg.Window('Мои инвестиции', layout, size=(sizeX, sizeY))

    while True:
        event, values = window.read()

        func_menu(event)

        if event in (sg.WIN_CLOSED, 'Quit'):
            break
    window.close()


def func_menu(event):
    if event == "Новости":
        get_list_news()
        return
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
    if event == "Операции по счету":
        doc = load_deposits_write_offs()
        wind_my_money(doc)
        return
    if event == "Мои активы":
        doc = load_deals()
        wind_my_deals(doc)
        return


def wind_table(list_data, list_columns, info):
    layout = [[sg.Table(values=list_data, headings=list_columns, def_col_width=20, max_col_width=50,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='lightyellow',
                        key='-TABLE_RU-',
                        selected_row_colors=('Black', 'GREEN'),
                        row_height=30,
                        tooltip=info)]]
    sg.theme('BlueMono')
    new_win = sg.Window(info, layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


def wind_my_money(doc):
    list_header, list_values, write_text = pars_doc_elem(doc)
    layout = [[sg.Text(size=(40, 5), key='out', text=write_text)],
              [sg.Table(values=list_values, headings=list_header, def_col_width=20, max_col_width=40,
                        background_color='lightblue',
                        text_color='Black',
                        auto_size_columns=True,
                        justification='centre',
                        num_rows=20,
                        alternating_row_color='lightyellow',
                        key='-TABLE_MONEY-',
                        selected_row_colors=('Black', 'GREEN'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои данные', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


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
                        alternating_row_color='lightyellow',
                        key='-TABLE_DEALS-',
                        selected_row_colors=('Black', 'GREEN'),
                        row_height=30)]
              ]
    sg.theme('BlueMono')
    new_win = sg.Window('Мои данные', layout)
    while True:
        event, values = new_win.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        new_win.close()


if __name__ == '__main__':
    main_wind()
