"""This module defines endpoints for user operations"""

import secrets
from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import unauthenticated_endpoint_wrapper, authenticated_endpoint_wrapper

from .bp import api_bp

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint to register a user"""

    def func(data):
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
                        authentication_token=token,
                        security_question=data["securityQuestion"],
                        security_question_answer=data["securityQuestionAnswer"])

        db.session.add(user)
        db.session.commit()

        # Return with the token
        return make_response({"token": token})

    return unauthenticated_endpoint_wrapper(create_user_schema, func)

create_user_schema = {
    "username": "username",
    "password": "hash",
    "securityQuestion": "int",
    "securityQuestionAnswer": "hash",
}

@api_bp.route('/users/questions', methods=['POST'])
def change_questions_authenticated():
    """Endpoint to let an authenticated user
    change their security questions"""

    def func(data, request_user_id):
        # Find a user by that username and security question hash
        res = UserModel.query.filter_by(id=request_user_id)

        # Update the token against that user
        res.update({UserModel.security_question: data["securityQuestion"],
                    UserModel.security_question_answer: data["securityQuestionAnswer"]})
        db.session.commit()

        # Return successful response
        return make_response()

    return authenticated_endpoint_wrapper(change_questions_authenticated_schema, func)

change_questions_authenticated_schema = {
    "securityQuestion": "int",
    "securityQuestionAnswer": "hash",
}

@api_bp.route('/users/password', methods=['POST'])
def change_password_authenticated():
    """Endpoint to let an authenticated user change their password"""

    def func(data, request_user_id):
        # Find a user by that username and security question hash
        res = UserModel.query.filter_by(id=request_user_id)

        # Update the token against that user
        res.update({UserModel.password_hash: data["password"]})
        db.session.commit()

        # Return successful response
        return make_response()

    return authenticated_endpoint_wrapper(change_password_authenticated_schema, func)

change_password_authenticated_schema = {
    "password": "hash",
}
