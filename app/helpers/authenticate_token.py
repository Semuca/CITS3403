"""This module provides authentication helper functions for api endpoints"""

from flask import request
from app.models import UserModel

def get_user_id_by_token():
    """Gets a user id by the token
    Returns:
        A user id if the token is stored against a user
        None otherwise
    """

    # Expected value of Authorization header: 'Bearer <token>'
    authorization_header = request.headers.get('Authorization').split()

    if len(authorization_header) != 2:
        return None

    token = authorization_header[1]

    res = UserModel.query.filter_by(authentication_token=token).first()

    return res.id if res is not None else None
