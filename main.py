"""This module is the entry point for the flask application"""

from flask import Flask

app = Flask(__name__)

#! Importing blueprint endpoints
#pylint: disable=wrong-import-position
from api import bp

app.register_blueprint(bp, url_prefix='/api')

@app.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"