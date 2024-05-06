"""Defines the thread object and provides functions to get and manipulate one"""

from datetime import datetime

from app.databases import db

# pylint: disable=too-few-public-methods
class ThreadModel(db.Model):
    """Represents a single post on the forum, stored in the 'threads' table in the DB"""

    __tablename__ = "threads"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    # Set fields
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = db.relationship("UserModel", backref="threads")
    children = db.relationship("CommentModel", backref="thread")

    # Currently here for testing purposes, to return representation of threads
    def to_json(self):
        """Return json from already-created thread object"""
        json_thread = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'createdAt': self.created_at,
            'user': self.user.to_json(),
            'children': [c.to_json() for c in self.children],
        }
        return json_thread
