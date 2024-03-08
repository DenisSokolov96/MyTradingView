'''
    pip freeze > requirements.txt
    pyi-makespec --onefile Main.py
    pyinstaller Main.spec
'''
import os
import sys
import warnings
import PySimpleGUI as sg
import requests

from AppLogger import file_logger
from GUI import main_wind, wind_error
from JSONRefact import load_json_files
from ReadPropertiTicket import load_properties

warnings.filterwarnings("ignore")


def check_net():
    try:
        response = requests.get("http://www.google.com")
        file_logger.info("интернет соединение устойчиво")
        return True
    except requests.ConnectionError:
        file_logger.warning("соединение с интернетом отсутствует")
        return False


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


if __name__ == '__main__':
    file_logger.info("Запуск приложения...")

    ico = resource_path(os.path.join('data', 'new_ico.ico'))
    sg.set_global_icon(ico)

    load_json_files()
    load_properties()

    if check_net():
        main_wind()
    else:
        wind_error()
