"""Defines the thread object and provides functions to get and manipulate one"""

from datetime import datetime

from main import db

class UserModel(db.Model):
    """Stores all users on the forum"""

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passwordHash = db.Column(db.String(200), nullable=False)
    authenticationToken = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime(), default=datetime.now, nullable=False)
