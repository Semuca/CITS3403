"""This module is the entry point for the flask application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)
    app.config['TESTING'] = True #TODO remove?

    # Configure app for db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app) 
    app.app_context().push()

    # Importing blueprint endpoints, avoiding circular imports
    #pylint: disable=wrong-import-position
    from api import bp

    app.register_blueprint(bp, url_prefix='/api')

    return app

app = createApp()
