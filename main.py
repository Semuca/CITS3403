"""This module is the entry point for the flask application"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    """A test 'hello world' function"""
    return "<p>Hello, World!</p>"
