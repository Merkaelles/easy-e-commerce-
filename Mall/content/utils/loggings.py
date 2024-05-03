import os
import logging
import logging.handlers
from flask import request


class ShopRequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr  # 客户端地址
        return super().format(record)


def create_logger(app):
    logging_level = app.config['LOGGING_LEVEL']
    logging_file_dir = app.config['LOGGING_FILE_DIR']
    logging_file_max_bytes = app.config['LOGGING_FILE_MAX_BYTES']
    logging_file_backup = app.config['LOGGING_FILE_BACKUP']

    if not os.path.isdir(logging_file_dir):
        os.mkdir(logging_file_dir)

    request_formatter = ShopRequestFormatter(
        '[%(asctime)s] %(remote_addr)s 请求 %(url)s \t %(levelname)s at %(module)s %(lineno)d : %(message)s')

    # 本地日志
    flask_file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(logging_file_dir, 'shop.log'),
                                                              maxBytes=logging_file_max_bytes,
                                                              backupCount=logging_file_backup)
    flask_file_handler.setFormatter(request_formatter)
    flask_logger = logging.getLogger('shop')
    flask_logger.addHandler(flask_file_handler)
    flask_logger.setLevel(logging_level)

    # 控制台日志
    flask_console_logger = logging.StreamHandler()
    flask_console_logger.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)s at %(module)s %(lineno)d : %(message)s'))
    if app.debug:
        flask_logger.addHandler(flask_console_logger)
