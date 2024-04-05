"""This module is the entry point for the flask application"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def createApp():
    """Create and configure app"""
    app = Flask(__name__)

    # Bind sqlalchemy db to app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/prod.db'
    db.init_app(app)

    # Importing blueprint endpoints
    #pylint: disable=wrong-import-position
    from api import bp
    app.register_blueprint(bp, url_prefix='/api')

    # Import and create dbs for models
    with app.app_context():
        #pylint: disable=wrong-import-position
        from models.thread import Thread
        from models.users import UserModel
        db.create_all()

    return app

def createTestApp():
    """Create and configure app for testing purposes"""
    app = Flask(__name__)
    app.config['TESTING'] = True

    # Bind sqlalchemy test db to app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/test.db'
    db.init_app(app)

    # Importing blueprint endpoints
    #pylint: disable=wrong-import-position
    from api import bp
    app.register_blueprint(bp, url_prefix='/api')

    # Import and create dbs for models
    with app.app_context():
        #pylint: disable=wrong-import-position
        from models.thread import Thread
        from models.users import UserModel
        db.create_all()

    return app

app = createApp()

@app.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"


@app.route("/login")
def login_page():
    """The login page"""

    user = {'username': 'Miguel'}
    return render_template('login.html', title='Home', user=user)

@app.route("/register")
def signup_page():
    """The login page"""

    user = {'username': 'Miguel'}
    return render_template('register.html', title='Home', user=user)