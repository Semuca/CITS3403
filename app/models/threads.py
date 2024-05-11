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
    comments = db.relationship("CommentModel", backref="thread")
    offers = db.relationship("OffersModel", backref="thread")

    @property
    def children(self) -> list:
        """All children (comments and trade offers) of this thread in date order"""
        return sorted(self.comments + self.offers, key=lambda x: x.created_at)

    # Currently here for testing purposes, to return representation of threads
    def to_json(self):
        """Return json from already-created thread object"""
        json_thread = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'createdAt': self.created_at,
            'user': self.user.to_json(),
        }
        return json_thread

    @staticmethod
    def thread_exists(thread_id: int) -> bool:
        """Check if a thread with this id exists"""
        return db.session.scalar(db.select(db.exists().where(ThreadModel.id == thread_id)))
