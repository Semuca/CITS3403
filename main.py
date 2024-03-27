"""This module is the entry point for the flask application"""

from flask import Flask, render_template

app = Flask(__name__)

#! Importing blueprint endpoints
#pylint: disable=wrong-import-position
from api import bp

app.register_blueprint(bp, url_prefix='/api')

@app.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"

@app.route("/login")
def login_page():
    """The login page"""

    user = {'username': 'Miguel'}
    return render_template('login.html', title='Home', user=user)
