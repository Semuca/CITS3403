"""This module provides authentication helper functions for api endpoints"""

import json
from typing import Callable
from flask import Response, make_response, redirect, request
from app.databases import db
from app.helpers.json_schema_validation import validate_request_schema
from app.models import LogModel, UserModel

def redirect_wrapper(successful_result: Response) -> Response:
    """Wrapper function to redirect to the login page if the user is not authenticated
    Returns:
        The parameter successful_result if the user is authenticated
        A redirect to the login page otherwise
    """

    token = request.cookies.get('token')

    if token is None or get_user_id_by_token(request.cookies.get('token')) is None:
        return redirect("/login")

    return successful_result

def get_user_id_by_auth_header() -> str | None:
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

def get_user_id_by_token(token: str) -> str | None:
    """Gets a user id by the token
    Returns:
        A user id if the token is stored against a user
        None otherwise
    """

    res = UserModel.query.filter_by(authentication_token=token).first()

    return res.id if res is not None else None

def authenticated_endpoint_wrapper(schema: dict[str, str], func: Callable[[dict[str, str], int], Response]) -> Response:
    """Performs the necessary checks for an authenticated endpoint"""

    # Authorize request
    request_user_id = get_user_id_by_auth_header()

    if request_user_id is None:
        return make_response(
            {"error": "Authorization error",
             "errorMessage": "Authorization token not valid"},
             401)

    # Get validated data
    data = None
    if schema is not None:
        data = validate_request_schema(schema)
        if isinstance(data, str):
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": data},
                 400)

    response = func(data, request_user_id)

    # Log the request
    new_log = LogModel(user_id=request_user_id,
                       url=request.full_path,
                       request_body=None if data is None else json.dumps(data),
                       response_code=response.status_code,
                       error_response_body=response.data if (response.status_code >= 400) else None)
    db.session.add(new_log)
    db.session.commit()

    return response

def unauthenticated_endpoint_wrapper(schema: dict[str, str], func: Callable[[dict[str, str]], Response]) -> Response:
    """Performs the necessary checks for an unauthenticated endpoint"""

    # Get validated data
    if schema is None:
        return func(None)

    data = validate_request_schema(schema)
    if isinstance(data, str):
        return make_response(
            {"error": "Request validation error",
             "errorMessage": data},
            400)

    return func(data)
