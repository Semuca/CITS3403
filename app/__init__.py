"""This module is the entry point for the flask application"""

from flask import Flask
from app.models import UserModel
from config import config

from .api import api_bp # Imports with all routes attached (as opposed to blank)
from .main import main_bp

from .databases import db

def create_app(config_name):
    """Create and configure app"""
    flask_app = Flask(__name__)
    flask_app.config.from_object(config.get(config_name or 'default'))

    # Bind sqlalchemy db to app
    db.init_app(flask_app)

    # Importing blueprint endpoints
    flask_app.register_blueprint(api_bp, url_prefix='/api')
    flask_app.register_blueprint(main_bp)

    # Import and create dbs for models
    with flask_app.app_context():
        db.create_all()

    return flask_app
