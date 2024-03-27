"""This module defines endpoints for user operations"""

import sqlite3

from api import bp
from common import validation

@bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to register a user"""

    data = validation.request_body_from_schema(createUserBodySchema)
    if isinstance(data, type("")):
        return {"error": "Request validation error", "errorMessage": data}


    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()

    # TODO (James): Prevent duplicates from being entered
    cursor.execute(f"INSERT INTO users VALUES ('{data["username"]}', '{data["password"]}')")

    db.commit()
    db.close()

    return "CREATED USER"

createUserBodySchema = {
    "username": "string",
    "password": "string",
}

@bp.route('/login', methods=['POST'])
def login():
    """Endpoint to let a user log in"""

    data = validation.request_body_from_schema(loginBodySchema)
    if isinstance(data, type("")):
        return {"error": "Request validation error", "errorMessage": data}

    # TODO (James): Constants for getting the database file
    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()

    res = cursor.execute(f"SELECT * FROM users WHERE username='{data["username"]}' AND passwordHash='{data["password"]}'")

    return res.fetchall()

loginBodySchema = {
    "username": "string",
    "password": "string",
}
