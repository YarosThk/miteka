import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///BookDb.db'
    DEBUG = True
    SECRET_KEY = 'gf3fcidc10f5ba23v56424fd191890w1'
    ENV = 'development'
