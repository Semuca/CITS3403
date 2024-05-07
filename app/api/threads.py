"""Defines endpoints for CRUD operations with threads"""

from flask import make_response

from app.databases import db
from app.models import ThreadModel
from app.helpers import authenticated_endpoint_wrapper

from .bp import api_bp

@api_bp.route('/threads', methods=['POST'])
def create_thread():
    """Creates a thread object and saves it to the database"""

    def func(data, request_user_id):
        # Create a thread object from parameters passed in
        new_thread = ThreadModel(title=data['title'],
            description=data['description'],
            user_id=request_user_id)

        # Save to db
        db.session.add(new_thread)
        db.session.commit()

        # Return for successful creation of resource
        return make_response(new_thread.to_json(), 201)

    return authenticated_endpoint_wrapper(create_thread_schema, func)

create_thread_schema = {
    "title": "text",
    "description": "text"
}

@api_bp.route('/threads', methods=['GET'])
def read_many_thread():
    """Reads a list of threads from the database based on query parameters"""

    def func(data, _):
        page = data.get("page", 1)
        per_page = data.get("perPage", 10)
        search = data.get("search", "")

        # Get a paginated list of thread objects according to parameters
        query = db.select(ThreadModel).filter(ThreadModel.title.contains(search))
        queried_threads = db.paginate(query, page=page, per_page=per_page).items

        # Return query result to client
        return make_response([ThreadModel.to_json(t) for t in queried_threads], 200)
    return authenticated_endpoint_wrapper(read_many_thread_schema, func)

read_many_thread_schema = {
    "page": {"type": "int", "required": False},
    "perPage": {"type": "int", "required": False},
    "search": {"type": "text", "required": False}
}

@api_bp.route('/threads/<int:thread_id>', methods=['GET'])
def read_by_id_thread(thread_id):
    """Reads the details of a thread object by its id"""

    def func(*_):
        # Get a thread object from the db according to given id
        queried_thread = db.session.get(ThreadModel, thread_id)

        if queried_thread is None:
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "Thread not found"},
                404)

        # Return query result to client
        return make_response(ThreadModel.to_json(queried_thread), 200)

    return authenticated_endpoint_wrapper(None, func)
