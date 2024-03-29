"""This module defines endpoints for user operations"""

import secrets
import sqlite3
from flask import make_response

from api import bp
from common import validation

@bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to register a user"""

    data = validation.request_body_from_schema(createUserBodySchema)
    if isinstance(data, type("")):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)


    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()

    token = secrets.token_urlsafe()

    res = cursor.execute(f"SELECT username FROM users WHERE username='{data["username"]}'")

    if (len(res.fetchall()) != 0):
        return make_response({"error": "Request validation error", "errorMessage": "User already exists"}, 403)


    cursor.execute(f"INSERT INTO users VALUES ('{data["username"]}', '{data["password"]}', '{token}')")

    db.commit()
    db.close()

    return make_response({"token": token})

createUserBodySchema = {
    "username": "string",
    "password": "string",
}

@bp.route('/login', methods=['POST'])
def login():
    """Endpoint to let a user log in"""

    data = validation.request_body_from_schema(loginBodySchema)
    if isinstance(data, type("")):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)

    # TODO (James): Constants for getting the database file
    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()

    res = cursor.execute(f"SELECT username FROM users WHERE username='{data["username"]}' AND passwordHash='{data["password"]}'")

    if (len(res.fetchall()) == 0):
        return make_response({"error": "Request validation error", "errorMessage": "User not found"}, 404)

    token = secrets.token_urlsafe()

    cursor.execute(f"UPDATE users SET accessToken='{token}' WHERE username='{data["username"]}' AND passwordHash='{data["password"]}'")

    return make_response({"token": token})

loginBodySchema = {
    "username": "string",
    "password": "string",
}
