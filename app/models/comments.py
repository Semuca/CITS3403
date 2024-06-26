"""Defines the comments object and provides functions to get and manipulate one"""

from datetime import datetime, timezone

from app.databases import db

# pylint: disable=too-few-public-methods
class CommentModel(db.Model):
    """Represents a single comment as part of a thread, stored in the 'comments' table in the DB"""

    __tablename__ = "comments"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Set fields
    comment_text = db.Column(db.Text(), nullable=False)
    thread_id = db.Column(db.Integer(), db.ForeignKey("threads.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = db.relationship("UserModel", backref="comments")
    thread_child_type = "comment"

    # Currently here for testing purposes, to return representation of comments
    def to_json(self):
        """Return json from already-created comment object"""
        json_comment = {
            'id': self.id,
            'childType': 'comment',
            'userId': self.user_id,
            'threadId': self.thread_id,
            'createdAt': self.created_at,
            'commentText': self.comment_text,
            'user': self.user.to_json(),
        }
        return json_comment
