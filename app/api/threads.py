"""Defines endpoints for CRUD operations with threads"""

from flask import make_response

from app.databases import db
from app.models import ThreadModel
from app.helpers import get_user_id_by_auth_header, validate_request_schema

from .bp import api_bp

@api_bp.route('/threads', methods=['POST'])
def create_thread():
    """Creates a thread object and saves it to the database"""

    # Validate post request schema
    data = validate_request_schema(create_thread_schema)
    if isinstance(data, str):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)

    # pylint: disable=duplicate-code
    # Authorize request
    request_user_id = get_user_id_by_auth_header()
    if request_user_id is None:
        return make_response(
            {"error": "Authorization error",
             "errorMessage": "Authorization token not valid"},
             401)

    # Create a thread object from parameters passed in
    new_thread = ThreadModel(title=data['title'],
        description=data['description'],
        user_id=request_user_id)

    # Save to db
    db.session.add(new_thread)
    db.session.commit()

    # Return for successful creation of resource
    return make_response(new_thread.to_json(), 201)

create_thread_schema = {
    "title": "string",
    "description": "string"
}

@api_bp.route('/threads', methods=['GET'])
def read_many_thread():
    """Reads a list of threads from the database based on query parameters"""

    # pylint: disable=duplicate-code
    # Authorize request
    request_user_id = get_user_id_by_auth_header()
    if request_user_id is None:
        return make_response(
            {"error": "Authorization error",
             "errorMessage": "Authorization token not valid"},
             401)

    # Get a list of thread objects according to parameters
    queried_threads = db.session.scalars(db.select(ThreadModel)).all() # to-do sorting and filtering later

    # Return query result to client
    return make_response([ThreadModel.to_json(t) for t in queried_threads], 200)


@api_bp.route('/threads/<int:thread_id>', methods=['GET'])
def read_by_id_thread(thread_id):
    """Reads the details of a thread object by its id"""

    # pylint: disable=duplicate-code
    # Authorize request
    request_user_id = get_user_id_by_auth_header()

    if request_user_id is None:
        return make_response(
            {"error": "Authorization error",
             "errorMessage": "Authorization token not valid"},
             401)

    # Get a thread object from the db according to given id
    queried_thread = db.session.get(ThreadModel, thread_id)

    if queried_thread is None:
        return make_response(
            {"error": "Request validation error",
             "errorMessage": "Thread not found"},
             404)

    # Return query result to client
    return make_response(ThreadModel.to_json(queried_thread), 200)
