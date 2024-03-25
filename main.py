"""This module is the entry point for the flask application"""

from flask import Flask, render_template, send_file, request, jsonify

app = Flask(__name__)

real_relational_database = {}


@app.route("/")
def hello_world():
    """A test 'hello world' function"""
    return "<p>Hello, World!</p>"


@app.route("/login")
def login_page():
    """Returns the login page that @jh1236 is working on"""
    if "token" in request.cookies:
        return f"<h1> YOUR TOKEN IS {request.cookies['token']}.  ENSURE YOU KEEP IT SECRET</h1>"
    return render_template("login.html")


@app.post("/api/create_account")
def create_account_endpoint():
    """The endpoint used to create an account"""
    real_relational_database[request.json["username"]] = request.json["password"]
    return "", 202


@app.post("/api/login")
def login_endpoint():
    print(request.json)
    if request.json["username"] not in real_relational_database:
        return "User Does not exist", 400
    if real_relational_database[request.json["username"]] == request.json["password"]:
        return jsonify({"token": 123456})
    else:
        return "Bad Password", 401
