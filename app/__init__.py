"""This module is the entry point for the flask application"""

from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect # Using this to half-manually-implement CSRF protection
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
    migrate = Migrate(flask_app, db, render_as_batch=True)
    migrate.init_app(flask_app, db, render_as_batch=True)

    # CSRF protection
    csrf = CSRFProtect(flask_app)
    csrf.init_app(flask_app)

    # Importing blueprint endpoints
    flask_app.register_blueprint(api_bp, url_prefix='/api')
    flask_app.register_blueprint(main_bp)

    return flask_app
