#from bookshelf.data.models import db, Role, User
#from flask_compress import Compress
#from flask_security import Security, SQLAlchemyUserDatastore
import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = 'postgres://agrofarmdb:agrofarmdb@localhost/testdb'
    SECRET_KEY = 'c13v-31op-m3n7-k3y'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'agrofarm.log'
    LOGGING_LEVEL = logging.DEBUG
    #SECURITY_CONFIRMABLE = False
    SQLALCHEMY_ECHO = True


    #CACHE_TYPE = 'simple'
    #COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', \
#'application/json', 'application/javascript']
    #COMPRESS_LEVEL = 6
    #COMPRESS_MIN_SIZE = 500
    #SUPPORTED_LANGUAGES = {'bg': 'Bulgarian', 'en': 'English', 'fr': 'Francais'}
    #BABEL_DEFAULT_LOCALE = 'en'
    #BABEL_DEFAULT_TIMEZONE = 'UTC'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgres://agrofarmdb:agrofarmdb@localhost/testdb'
    SECRET_KEY = 'c13v-31op-m3n7-k3y'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://agrofarmdb:agrofarmdb@localhost/testdb'
    SECRET_KEY = 'c13v-31op-m3n7-k3y'

config = {
    "development": "agrofarm.config.DevelopmentConfig",
    "testing": "agrofarm.config.TestingConfig",
    "default": "agrofarm.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # Configure Security
    #user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    #app.security = Security(app, user_datastore)
    # Configure Compressing
    #Compress(app)
