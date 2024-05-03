# configuration

class Config:
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'test'
    USERNAME = 'root'
    PASSWORD = 'uckingdom'
    DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不需要追踪数据的修改

    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FILE_DIR = 'logs/'
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024
    LOGGING_FILE_BACKUP = 100

    RATELIMIT_STORAGE_URL = 'redis://192.168.183.128:6379/0'  # 限流信息临时存储 by redis
    RATELIMIT_STRATEGY = 'moving-window'

    REDIS_URL = 'redis://192.168.183.128:6379/1'

    PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductConfig(Config):
    pass
