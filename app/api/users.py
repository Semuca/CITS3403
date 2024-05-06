"""This module defines endpoints for user operations"""

import secrets
from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import authenticated_endpoint_wrapper, remove_none_from_dictionary, unauthenticated_endpoint_wrapper

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
                        description="",
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

@api_bp.route('/users', methods=['PUT'])
def edit_user():
    """Endpoint to let an authenticated user
    change their information"""

    def func(data, request_user_id):
        # Find a user by that username and security question hash
        res = UserModel.query.filter_by(id=request_user_id)

        update_body = { UserModel.description: data.get("description"),
                        UserModel.password_hash: data.get("password"),
                        UserModel.security_question: data.get("securityQuestion"),
                        UserModel.security_question_answer: data.get("securityQuestionAnswer")}

        # Update the token against that user
        res.update(remove_none_from_dictionary(update_body))
        db.session.commit()

        # Return successful response
        return make_response()

    return authenticated_endpoint_wrapper(change_questions_authenticated_schema, func)

change_questions_authenticated_schema = {
    "description": {"type": "text", "required": False},
    "password": {"type": "hash", "required": False},
    "securityQuestion": {"type": "int", "required": False},
    "securityQuestionAnswer": {"type": "hash", "required": False},
}
