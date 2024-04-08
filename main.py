"""This module is the entry point for the flask application"""

from flask import Flask, render_template

# Imports api with all routes attached (as opposed to just importing the blank blueprint)
from api import bp
from threads import threads_bp
from databases.db import db

# pylint: disable=unused-import
import models

def create_app():
    """Create and configure app"""
    flask_app = Flask(__name__)

    # Bind sqlalchemy db to app
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{flask_app.root_path}/prod.db'
    db.init_app(flask_app)

    # Importing blueprint endpoints
    flask_app.register_blueprint(bp, url_prefix='/api')
    flask_app.register_blueprint(threads_bp, url_prefix='/api')

    # Import and create dbs for models
    with flask_app.app_context():
        db.create_all()

    return flask_app

def create_test_app():
    """Create and configure app for testing purposes"""
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = True

    # Bind sqlalchemy test db to app
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{flask_app.root_path}/test.db'
    db.init_app(flask_app)

    # Importing blueprint endpoints
    flask_app.register_blueprint(bp, url_prefix='/api')
    flask_app.register_blueprint(threads_bp, url_prefix='/api')

    # Import and create dbs for models
    with flask_app.app_context():
        db.create_all()

    return flask_app

app = create_app()

@app.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"

@app.route("/login")
def login_page():
    """The login page"""

    return render_template('login.html', title='Home')

@app.route("/register")
def signup_page():
    """The login page"""

    return render_template('register.html', title='Home')
