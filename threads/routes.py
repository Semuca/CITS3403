"""Defines endpoints for CRUD operations with threads"""

from flask import request, make_response

from threads import threads_bp
from helpers.json_schema_validation import validate_request_schema
from models.thread import ThreadModel
from databases.db import db

@threads_bp.route('/threads', methods=['POST'])
def create_thread():
    # Validate post request schema
    data = validate_request_schema(create_thread_schema)
    if isinstance(data, type("")):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)

    # Create a thread object from parameters passed in
    new_thread = ThreadModel.from_json(data)

    # Save to db
    db.session.add(new_thread)
    db.session.commit()

    # Return for successful creation of resource
    return make_response(new_thread.to_json(), 201)

create_thread_schema = {
    "title": "string",
    "description": "string",
    "userId": "int"
}

@threads_bp.route('/threads', methods=['GET'])
def read_many_thread():
    # Get a list of thread objects according to parameters
    queried_threads = ThreadModel.query.all() # currently just gets all threads - sorting and filtering TODO

    # Return query result to client
    return make_response([ThreadModel.to_json(t) for t in queried_threads], 200)