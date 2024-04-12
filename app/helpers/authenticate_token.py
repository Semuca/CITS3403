"""This module provides authentication helper functions for api endpoints"""

from flask import redirect, request
from app.models import UserModel

def auth_redirect(successful_result):
    """Wrapper function to redirect to the login page if the user is not authenticated
    Returns:
        The parameter successful_result if the user is authenticated
        A redirect to the login page otherwise
    """

    token = request.cookies.get('token')

    if token is None or get_user_id_by_token(request.cookies.get('token')) is None:
        return redirect("/login")

    return successful_result

def get_user_id_by_auth_header():
    """Gets a user id by the Authorization header
    Returns:
        A user id if the token is stored against a user
        None otherwise
    """

    # Expected value of Authorization header: 'Bearer <token>'
    authorization_header = request.headers.get('Authorization')
    if authorization_header is None:
        return None

    split_authorization_header = authorization_header.split()

    if len(split_authorization_header) != 2:
        return None

    token = split_authorization_header[1]

    return get_user_id_by_token(token)

def get_user_id_by_token(token):
    """Gets a user id by the token
    Returns:
        A user id if the token is stored against a user
        None otherwise
    """

    res = UserModel.query.filter_by(authentication_token=token).first()

    return res.id if res is not None else None
