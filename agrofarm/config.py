import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # sqlite :memory: identifier is the default if no filepath is present
    SQLALCHEMY_DATABASE_URI = "postgres://agrofarmdb:agrofarmdb@localhost/testdb"
    SECRET_KEY = "c13v-31op-m3n7-k3y"
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "agrofarm.log"
    LOGGING_LEVEL = logging.DEBUG
    # SECURITY_CONFIRMABLE = False
    SQLALCHEMY_ECHO = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgres://agrofarmdb:agrofarmdb@localhost/testdb"
    SECRET_KEY = "c13v-31op-m3n7-k3y"
    JSON_AS_ASCII = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgres://agrofarmdb:agrofarmdb@localhost/testdb"
    SECRET_KEY = "c13v-31op-m3n7-k3y"
    JSON_AS_ASCII = False


config = {
    "development": "agrofarm.config.DevelopmentConfig",
    "testing": "agrofarm.config.TestingConfig",
    "default": "agrofarm.config.DevelopmentConfig",
}


def configure_app(app):
    config_name = os.getenv("FLASK_CONFIGURATION", "testing")
    app.config.from_object(config[config_name])
    app.config.from_pyfile("config.cfg", silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config["LOGGING_LOCATION"])
    handler.setLevel(app.config["LOGGING_LEVEL"])
    formatter = logging.Formatter(app.config["LOGGING_FORMAT"])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
