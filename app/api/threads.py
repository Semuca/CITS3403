"""Defines endpoints for CRUD operations with threads"""

from flask import make_response

from app.databases import db
from app.models import ThreadModel
from app.helpers.json_schema_validation import validate_request_schema

from .bp import api_bp

@api_bp.route('/threads', methods=['POST'])
def create_thread():
    """Creates a thread object and saves it to the database"""
    # Validate post request schema
    data = validate_request_schema(create_thread_schema)
    if isinstance(data, str):
        return make_response({"error": "Request validation error", "errorMessage": data}, 400)

    # Create a thread object from parameters passed in
    new_thread = ThreadModel(title=data['title'],
        description=data['description'],
        user_id=data['userId'])

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

@api_bp.route('/threads', methods=['GET'])
def read_many_thread():
    """Reads a list thread objects from the database based on query parameters"""

    # Get a list of thread objects according to parameters
    queried_threads = ThreadModel.query.all() # to-do sorting and filtering later

    # Return query result to client
    return make_response([ThreadModel.to_json(t) for t in queried_threads], 200)
