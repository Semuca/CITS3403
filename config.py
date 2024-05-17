"""Flask app configurations"""

from datetime import timedelta
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

    # CSRF protection
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_HEADERS = ['X-CSRFTOKEN']

    # Game mechanics
    LEVEL_EXPIRY_TIMER = timedelta(days=1)
    LOOT_DROP_TIMER = timedelta(hours=12)


# pylint: disable=too-few-public-methods
class DevConfig(Config):
    """Config for the development environment"""

    # Databases
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'databases', 'dev.db')

    # CSRF protection
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True

    # Game mechanics
    LEVEL_EXPIRY_TIMER = timedelta(minutes=2)
    LOOT_DROP_TIMER = timedelta(minutes=1)

# pylint: disable=too-few-public-methods
class ProdConfig(Config):
    """Config for the production environment"""

    # Databases
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app', 'databases', 'prod.db')

    # CSRF protection
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True

    # Game mechanics
    LEVEL_EXPIRY_TIMER = timedelta(days=1)
    LOOT_DROP_TIMER = timedelta(hours=12)

config = {
    'default': DevConfig,
    'test': TestConfig,
    'dev': DevConfig,
    'prod': ProdConfig
}
