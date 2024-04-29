"""This module defines endpoints for user operations"""

import secrets
from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import unauthenticated_endpoint_wrapper

from .bp import api_bp

@api_bp.route('/login', methods=['POST'])
def login():
    """Endpoint to let a user log in"""

    def func(data):
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

    return unauthenticated_endpoint_wrapper(login_schema, func)

login_schema = {
    "username": "username",
    "password": "hash",
}

@api_bp.route('/login/questions', methods=['POST'])
def change_password_with_questions():
    """Endpoint to let a user change their forgotten
    password through security questions"""

    def func(data):
        # Find a user by that username and security question hash
        res = UserModel.query.filter_by(username=data["username"], security_question_answer=data["securityQuestionAnswer"])

        # If the user is not found, return a 404
        if res.first() is None:
            return make_response({"error": "Request validation error",
                                "errorMessage": "User not found"},
                                404)

        # Create token
        token = secrets.token_urlsafe()

        # Update the token against that user
        res.update({UserModel.change_password_token: token})
        db.session.commit()

        # Return with the token
        return make_response({"token": token})

    return unauthenticated_endpoint_wrapper(change_password_with_questions_schema, func)

change_password_with_questions_schema = {
    "username": "username",
    "securityQuestionAnswer": "hash",
}

@api_bp.route('/login/password', methods=['POST'])
def change_password_unauthenticated():
    """Endpoint to let a user change their forgotten
    password with a change password token"""

    def func(data):
        # Find a user by that username and security question hash
        res = UserModel.query.filter_by(change_password_token=data["changePasswordToken"])

        # If the user is not found, return a 404
        if res.first() is None:
            return make_response({"error": "Request validation error",
                                "errorMessage": "User not found"},
                                404)

        # Create token
        token = secrets.token_urlsafe()

        # Update the token against that user
        res.update({UserModel.password_hash: data["password"], UserModel.change_password_token: None, UserModel.authentication_token: token})
        db.session.commit()

        # Return with the token
        return make_response({"token": token})

    return unauthenticated_endpoint_wrapper(change_password_unauthenticated_schema, func)

change_password_unauthenticated_schema = {
    "password": "hash",
    "changePasswordToken": "text",
}
