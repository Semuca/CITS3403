"""Defines endpoints for CRUD operations with comments"""

from flask import make_response

from app.databases import db
from app.models import CommentModel
from app.helpers import get_user_id_by_auth_header, validate_request_schema

from .bp import api_bp

@api_bp.route('/threads/<int:thread_id>/comments', methods=['POST'])
def create_comment(thread_id):
    """Creates a comment object for a thread and saves it to the database"""

    # Validate post request schema
    data = validate_request_schema(create_comment_schema)
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

    # Create a comment object from parameters passed in
    new_comment = CommentModel(
        user_id=request_user_id,
        thread_id=thread_id,
        data=data['data']
    )

    # Save to db
    db.session.add(new_comment)
    db.session.commit()

    # Return for successful creation of resource
    return make_response(new_comment.to_json(), 201)

create_comment_schema = {
    "data": "string"
}

@api_bp.route('/threads/<int:thread_id>/children', methods=['GET'])
def read_many_comment(thread_id):
    """Reads a list of comments from the database for the thread"""

    # pylint: disable=duplicate-code
    # Authorize request
    request_user_id = get_user_id_by_auth_header()
    if request_user_id is None:
        return make_response(
            {"error": "Authorization error",
             "errorMessage": "Authorization token not valid"},
             401)

    # Get a list of comment objects in the thread in order of creation
    queried_threads = db.session.scalars(
        db.select(CommentModel)
        .where(CommentModel.thread_id == thread_id)
        .order_by(CommentModel.created_at.asc())
    ).all()

    # Return query result to client
    return make_response([CommentModel.to_json(t) for t in queried_threads], 200)
