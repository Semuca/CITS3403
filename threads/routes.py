"""Defines endpoints for CRUD operations with threads"""

from flask import request, make_response

from threads import threads_bp
from models.thread import ThreadModel

from main import db

@threads_bp.route('/threads', methods=['POST'])
def create_thread():
    # Create a thread object from parameters passed in
    try:
        new_thread = ThreadModel.from_json(request.json)
    except Exception as err:
        return make_response({"error": "Request validation error", "errorMessage": str(err)}, 400)

    # Save to db
    db.session.add(new_thread)
    db.session.commit()

    # Return for successful creation of resource
    return make_response(new_thread.to_json(), 201)

@threads_bp.route('/threads', methods=['GET'])
def read_many_thread():
    # Get a list of thread objects according to parameters
    queried_threads = ThreadModel.query.all() # currently just gets all threads - sorting and filtering TODO

    # Return query result to client
    return make_response([ThreadModel.to_json(t) for t in queried_threads], 200)