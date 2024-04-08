"""Flask app configurations"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# pylint: disable=too-few-public-methods
class Config:
    """General base config class"""

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

# pylint: disable=too-few-public-methods
class TestConfig(Config):
    """Config for a testing environment"""

    # General config
    DEBUG = True
    TESTING = True

    # Databases
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'databases', 'test.db')

# pylint: disable=too-few-public-methods
class DevConfig(Config):
    """Config for the development environment"""

    # Databases
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'databases', 'dev.db')

config = {
    'default': DevConfig,
    'test': TestConfig,
    'dev': DevConfig,
}