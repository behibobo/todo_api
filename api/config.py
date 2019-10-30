"""
    config.py
    - settings for the flask application object
"""

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = 'mysupersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///items.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
