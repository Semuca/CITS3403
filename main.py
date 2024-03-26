"""This module is the entry point for the flask application"""

import json
import sqlite3
from flask import Flask, render_template, Blueprint, request

app = Flask(__name__)
bp = Blueprint('api', __name__)

@bp.route('/login', methods=['POST'])
def login():
    # TODO (James): Schema validation for requests
    data = request.get_json()
    
    # TODO (James): Constants for getting the database file
    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()
    
    res = cursor.execute(f"SELECT * FROM users WHERE username='{data["username"]}'")
    
    return res.fetchone()

@bp.route('/register', methods=['POST'])
def register():
    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()
    
    # TODO (James): Prevent duplicates from being entered
    cursor.execute("INSERT INTO users VALUES ('username', 'password')")
    
    db.commit()
    
    return "CREATED USER"

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