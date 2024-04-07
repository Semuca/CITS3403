"""This module is the entry point for the flask application"""

from flask import Flask

from api import bp
from databases.db import db

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
        #pylint: disable=wrong-import-position
        # from models.thread import Thread
        # from models.users import UserModel
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
        #pylint: disable=wrong-import-position
        # from models.thread import Thread
        # from models.users import UserModel
        db.create_all()

    return app

flaskApp = create_app()
