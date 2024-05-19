"""This module defines endpoints for user operations"""

import secrets

from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import authenticated_endpoint_wrapper, remove_none_from_dictionary, unauthenticated_endpoint_wrapper, \
    RequestSchemaDefinition
from app.helpers.levelling import auto_level

from .bp import api_bp


@api_bp.route('/users', methods=['GET'])
def get_user():
    """Endpoint to get the current user through the authentication token"""

    def func(_data, request_user_id):
        # Get a thread object from the db according to given id
        queried_user = db.session.get(UserModel, request_user_id)

        # Checks if time is up and performs auto level ups/downs if necessary
        auto_level(queried_user)

        # Return user to the client
        return make_response(UserModel.to_json(queried_user), 200)

    return authenticated_endpoint_wrapper(None, func)


@api_bp.route('/users/<username>/question', methods=['GET'])
def get_user_question(username):
    """Endpoint to get the current user's choice in security question"""

    def func(_data):
        # Get the user by username
        queried_user = UserModel.query.filter_by(username=username).first()


        # Return user to the client
        return make_response({"question": queried_user.security_question}, 200)

    return unauthenticated_endpoint_wrapper(None, func)



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
        return make_response({"id": user.id, "token": token})

    return unauthenticated_endpoint_wrapper(create_user_schema, func)


create_user_schema: dict[str, str | RequestSchemaDefinition] = {
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
        res = UserModel.query.filter_by(id=request_user_id)  # the query, not the query result

        update_body = {UserModel.description: data.get("description"),
                       UserModel.password_hash: data.get("password"),
                       UserModel.security_question: data.get("securityQuestion"),
                       UserModel.security_question_answer: data.get("securityQuestionAnswer")}

        # Update the token against that user
        res.update(remove_none_from_dictionary(update_body))
        db.session.commit()

        # Return successful response
        return make_response()

    return authenticated_endpoint_wrapper(change_questions_authenticated_schema, func)


change_questions_authenticated_schema: dict[str, str | RequestSchemaDefinition] = {
    "description": {"type": "text", "required": False},
    "password": {"type": "hash", "required": False},
    "securityQuestion": {"type": "int", "required": False},
    "securityQuestionAnswer": {"type": "hash", "required": False},
}
