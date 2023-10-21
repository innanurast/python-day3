import os
from decouple import config
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    DEBUG = config('DEBUG', cast=bool)
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
    SQLALCHEMY_ECHO = config('SQLALCHEMY_ECHO', cast=bool)

class Devconfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/latihanapi'
    SQLALCHEMY_RECORD_QUERIES = config('SQLACHEMY_RECORD_QUERIES', cast=bool)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=0)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class Qasconfig(Config):
    pass

class Prdconfig(Config):
    pass

config_dict = {
    'dev': Devconfig,
    'qas': Qasconfig,
    'prd': Prdconfig,
}