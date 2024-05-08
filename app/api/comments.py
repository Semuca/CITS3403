"""Defines endpoints for CRUD operations with comments"""

from flask import make_response

from app.databases import db
from app.models import ThreadModel, CommentModel
from app.helpers import authenticated_endpoint_wrapper, RequestSchemaDefinition

from .bp import api_bp

@api_bp.route('/threads/<int:thread_id>/comments', methods=['POST'])
def create_comment(thread_id):
    """Creates a comment object for a thread and saves it to the database"""

    def func(data, request_user_id):
        # Check that a thread with this id does exist
        if not db.session.scalar(db.select(db.exists().where(ThreadModel.id == thread_id))):
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "Thread not found"},
                404)

        # Create a comment object from parameters passed in
        new_comment = CommentModel(
            user_id=request_user_id,
            thread_id=thread_id,
            comment_text=data['commentText']
        )

        # Save to db
        db.session.add(new_comment)
        db.session.commit()

        # Return for successful creation of resource
        return make_response(new_comment.to_json(), 201)

    return authenticated_endpoint_wrapper(create_comment_schema, func)

create_comment_schema: dict[str, str | RequestSchemaDefinition] = {
    "commentText": "text"
}

@api_bp.route('/threads/<int:thread_id>/children', methods=['GET'])
def read_many_comment(thread_id):
    """Reads a list of comments from the database for the thread"""

    def func(*_):
        # Check that a thread with this id does exist
        if not db.session.scalar(db.select(db.exists().where(ThreadModel.id == thread_id))):
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "Thread not found"},
                404)

        # Get a list of comment objects in the thread in order of creation
        queried_comments = db.session.scalars(
            db.select(CommentModel)
            .where(CommentModel.thread_id == thread_id)
            .order_by(CommentModel.created_at.asc())
        ).all()

        # Return query result to client
        return make_response([CommentModel.to_json(t) for t in queried_comments], 200)

    return authenticated_endpoint_wrapper(None, func)
