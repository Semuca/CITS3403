"""This module is the entry point for the flask application"""

from flask import Flask

# Imports api with all routes attached (as opposed to just importing the blank blueprint)
from api import bp
from databases.db import db

# pylint: disable=unused-import
import models

def create_app():
    """Create and configure app"""
    app = Flask(__name__)

    # Bind sqlalchemy db to app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/prod.db'
    db.init_app(app)

    # Importing blueprint endpoints
    app.register_blueprint(bp, url_prefix='/api')

    # Import and create dbs for models
    with app.app_context():
        db.create_all()

    return app

def create_test_app():
    """Create and configure app for testing purposes"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Bind sqlalchemy test db to app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/test.db'
    db.init_app(app)

    # Importing blueprint endpoints
    app.register_blueprint(bp, url_prefix='/api')

    # Import and create dbs for models
    with app.app_context():
        db.create_all()

    return app

flaskApp = create_app()
