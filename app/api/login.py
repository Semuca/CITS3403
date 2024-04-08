"""This module defines endpoints for user operations"""

import secrets
from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import validate_request_schema

from .bp import api_bp

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to register a user"""

    # Get validated data
    data = validate_request_schema(create_user_schema)
    if isinstance(data, str):
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
                     password_hash=data["password"],
                     authentication_token=token)
    db.session.add(user)
    db.session.commit()

    # Return with the token
    return make_response({"token": token})

create_user_schema = {
    "username": "username",
    "password": "password",
}

@api_bp.route('/login', methods=['POST'])
def login():
    """Endpoint to let a user log in"""

    # Get validated data
    data = validate_request_schema(login_schema)
    if isinstance(data, str):
        return make_response(
            {"error": "Request validation error",
             "errorMessage": data},
            400)

    # Find a user by that username and password hash
    res = UserModel.query.filter_by(username=data["username"],
                                    password_hash=data["password"])

    # If the user is not found, return a 404
    if res.first() is None:
        return make_response({"error": "Request validation error",
                              "errorMessage": "User not found"},
                             404)

    # Create token
    token = secrets.token_urlsafe()

    # Update the token against that user
    res.update({UserModel.authentication_token: token})
    db.session.commit()

    # Return with the token
    return make_response({"token": token})

login_schema = {
    "username": "username",
    "password": "password",
}
