"""Defines the users object and provides functions to get and manipulate one"""

from datetime import datetime

from app.databases import db

# pylint: disable=too-few-public-methods
class UserModel(db.Model):
    """Stores all users on the forum"""

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passwordHash = db.Column(db.String(200), nullable=False)
    authenticationToken = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime(), default=datetime.now, nullable=False)
