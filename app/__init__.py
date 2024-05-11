"""This module is the entry point for the flask application"""

from flask import Flask
from flask_migrate import Migrate
from app import models
from config import config

from .api import api_bp # Imports with all routes attached (as opposed to blank)
from .main import main_bp

from .databases import db # sqlalchemy db defined here to avoid circular imports

def create_app(config_name='default'):
    """Create and configure app"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(config.get(config_name))

    # Bind sqlalchemy db to app
    db.init_app(flask_app)

    # Bind migration to app
    migrate = Migrate(flask_app, db)
    migrate.init_app(flask_app, db)

    # Importing blueprint endpoints
    flask_app.register_blueprint(api_bp, url_prefix='/api')
    flask_app.register_blueprint(main_bp)

    return flask_app
