"""Defines the thread object and provides functions to get and manipulate one"""

from datetime import datetime

from app.databases import db

class ThreadModel(db.Model):
    """Represents a single post on the forum, stored in the 'threads' table in the DB"""

    __tablename__ = "threads"

    id = db.Column(db.Integer(), primary_key=True)
    createdAt = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    userId = db.Column(db.Integer(), nullable=False) #to do add relationship to users table; set in backend to current user

    def to_json(self):
        """Return json from already-created thread object"""
        json_thread = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'createdAt': self.createdAt,
            'userId': self.userId,
        }
        return json_thread
