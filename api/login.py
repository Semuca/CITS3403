import sqlite3

from api import bp
from common import validation

@bp.route('/users', methods=['POST'])
def create_user():
    data = validation.requestBodyFromSchema(createUserBodySchema)
    if (isinstance(data, type(""))):
        return {"error": "Request validation error", "errorMessage": data}
    
    
    db = sqlite3.connect("databases/database.db")
    cursor = db.cursor()
    
    # TODO (James): Prevent duplicates from being entered
    cursor.execute(f"INSERT INTO users VALUES ('{data["username"]}', '{data["passwordHash"]}')")
    
    db.commit()
    
    return "CREATED USER"

createUserBodySchema = {
    "username": "string",
    "password": "string",
}

@bp.route('/login', methods=['POST'])
def login():
    data = validation.requestBodyFromSchema(loginBodySchema)
    if (isinstance(data, type(""))):
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