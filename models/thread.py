"""Defines the thread object and provides functions to get and manipulate one"""

from datetime import datetime

from main import db

class Thread(db.Model):
    """Represents a single post on the forum, stored in the 'threads' table in the DB"""

    __tablename__ = "threads"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    createdAt = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    userId = db.Column(db.Integer(), nullable=False) #TODO add as foreign key to users table
