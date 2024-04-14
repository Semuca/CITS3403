"""Defines the comments object and provides functions to get and manipulate one"""

from datetime import datetime

from app.databases import db

# pylint: disable=too-few-public-methods
class CommentModel(db.Model):
    """Represents a single comment as part of a thread, stored in the 'comments' table in the DB"""

    __tablename__ = "comments"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    # Set fields
    comment_text = db.Column(db.Text(), nullable=False)
    thread_id = db.Column(db.Integer(), db.ForeignKey("threads.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    # Currently here for testing purposes, to return representation of comments
    def to_json(self):
        """Return json from already-created comment object"""
        json_comment = {
            'id': self.id,
            'userId': self.user_id,
            'threadId': self.thread_id,
            'createdAt': self.created_at,
            'commentText': self.comment_text,
        }
        return json_comment
