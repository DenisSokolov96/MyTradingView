import os
from lxml import etree
import PySimpleGUI as sg
import pandas as pd

from Assets import Assets

assets = Assets()
path_to_file = 'dataXML/UserInfo.xml'


# Прочитать из XML пути для парсинга файлов брокера
def load_xml_files():
    try:
        list_deal = []
        list_transaction = []
        for event, elem in etree.iterparse(path_to_file):
            if elem.tag == "deal":
                list_deal.append(elem.text)
            if elem.tag == "transaction":
                list_transaction.append(elem.text)
        send_to_read_data(list_deal, list_transaction)
    except:
        os.makedirs('dataXML', exist_ok=True)
        root = etree.Element("root")
        etree.SubElement(root, "deals")
        etree.SubElement(root, "transactions")
        tree = etree.ElementTree(root)
        tree.write(path_to_file, pretty_print=True, encoding="utf-8", xml_declaration=True)


# Прочитать и записать данные в память
def send_to_read_data(list_deal, list_transaction):
    if len(list_deal) > 0:
        assets.doc_deals = pd.read_excel(list_deal[0])
    if len(list_transaction) > 0:
        assets.deposits_write_offs = pd.read_excel(list_transaction[0])


# Открыть проводник
def set_path(name_doc):
    ftypes = [('Документы по' + name_doc, '*.xlsx'), ('Документы', '*.xls'), ('Все файлы', '*')]
    dlg = sg.filedialog.Open(filetypes=ftypes)
    fl = dlg.show()
    if fl != '':
        return fl
    return ''


# Запись путей к файлу для парсинга в XML
def write_to_xml(path_deals, path_trans):
    if path_deals != '':
        tree = etree.parse(path_to_file)
        condition_elem = tree.find("deals")
        etree.SubElement(condition_elem, 'deal').text = path_deals
        tree.write(path_to_file, pretty_print=True, encoding='utf-8', xml_declaration=True)
    if path_trans != '':
        tree = etree.parse(path_to_file)
        condition_elem = tree.find("transactions")
        etree.SubElement(condition_elem, 'transaction').text = path_trans
        tree.write(path_to_file, pretty_print=True, encoding='utf-8', xml_declaration=True)
    load_xml_files()
