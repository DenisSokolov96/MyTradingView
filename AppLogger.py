import logging

file_logger = logging.getLogger()
file_logger.setLevel(logging.INFO)
path_to_file = 'data/logFileAppInvest.log'
handler = logging.FileHandler(path_to_file, 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
file_logger.addHandler(handler)
