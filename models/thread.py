"""Defines the thread object and provides functions to get and manipulate one"""

from datetime import datetime
from flask import request
from sqlalchemy.orm import validates

from main import db

class ThreadModel(db.Model):
    """Represents a single post on the forum, stored in the 'threads' table in the DB"""

    __tablename__ = "threads"

    id = db.Column(db.Integer(), primary_key=True)
    createdAt = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    userId = db.Column(db.Integer(), nullable=False)
    #TODO add userId as foreign key to users table, also set in backend to current user

    @validates('title')
    def validate_title(self, key, value):
        if value is None or value == '':
            raise Exception(f"Required field '{key}' missing")
        return value

    @validates('description')
    def validate_description(self, key, value):
        if value is None or value == '':
            raise Exception(f"Required field '{key}' missing")
        return value

    @validates('userId')
    def validate_userId(self, key, value):
        if value is None or value == '':
            raise Exception(f"Required field '{key}' missing")
        if not value.isdigit():
            raise Exception(f"{key} field must be an integer")
        return value

    # def validate_json(json_thread):
    #     for field, value in json_thread:


    """Creates a thread from json"""
    def from_json(self, json_thread):
        # Get json thread information
        title = json_thread['title']
        description = json_thread['description']
        userId = json_thread['userId']

        # Try creating thread from info
        try:
            new_thread = ThreadModel(title=title, description=description, userId=userId)
        except Exception as err:
            raise Exception(err)

        return new_thread

    """Get json from already-created thread object"""
    def to_json(self):
        json_thread = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'createdAt': self.createdAt,
            'userId': self.userId,
        }
        return json_thread

