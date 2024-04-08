"""Main route views"""

from flask import render_template

from . import main_bp

@main_bp.route("/")
def hello_world():
    """A test 'hello world' function"""

    return "<p>Hello, World!</p>"

@main_bp.route("/login")
def login_page():
    """The login page"""

    return render_template('login.html', title='Home')

@main_bp.route("/register")
def signup_page():
    """The login page"""

    return render_template('register.html', title='Home')
