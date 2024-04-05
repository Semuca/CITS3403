"""This module defines endpoints for user operations"""

import secrets
from flask import make_response

from api import bp
from helpers.json_schema_validation import validate_request_schema
from main import db
from models.users import UserModel

@bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to register a user"""

    # Get validated data
    data = validate_request_schema(createUserBodySchema)
    if isinstance(data, type("")):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)

    # Find if a user by that username already exists
    res = UserModel.query.filter_by(username=data["username"]).first()

    if res is not None:
        return make_response(
            {"error": "Request validation error",
             "errorMessage": "User already exists"},
            403)

    # Create token
    token = secrets.token_urlsafe()

    # Add the user into the database
    user = UserModel(username=data["username"],
                     passwordHash=data["password"],
                     authenticationToken=token)
    db.session.add(user)
    db.session.commit()

    # Return with the token
    return make_response({"token": token})

createUserBodySchema = {
    "username": "string",
    "password": "string",
}

@bp.route('/login', methods=['POST'])
def login():
    """Endpoint to let a user log in"""

    # Get validated data
    data = validate_request_schema(loginBodySchema)
    if isinstance(data, type("")):
        return make_response(
            {"error": "Request validation error",
             "errorMessage": data},
            400)

    # Find a user by that username and passwordHash
    res = UserModel.query.filter_by(username=data["username"],
                                    passwordHash=data["password"])


    # If the user is not found, return a 404
    if res.first() is None:
        return make_response({"error": "Request validation error",
                              "errorMessage": "User not found"},
                             404)

    # Create token
    token = secrets.token_urlsafe()

    # Update the token against that user
    res.update({UserModel.authenticationToken: token})
    db.session.commit()

    # Return with the token
    return make_response({"token": token})

loginBodySchema = {
    "username": "string",
    "password": "string",
}
