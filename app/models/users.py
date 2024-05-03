"""Defines the users object and provides functions to get and manipulate one"""

from datetime import datetime

from app.databases import db

# pylint: disable=too-few-public-methods
class UserModel(db.Model):
    """Stores all users on the forum"""

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    password_hash = db.Column(db.String(200), nullable=False)
    authentication_token = db.Column(db.String(200))
    change_password_token = db.Column(db.String(200))
    security_question = db.Column(db.String(200), nullable=False)
    security_question_answer = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    def to_json(self):
        """Return json from already-created user object"""
        json_user = {
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'createdAt': self.created_at,
        }
        return json_user
