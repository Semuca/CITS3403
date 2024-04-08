"""This module stores the databases for the flask application separately to avoid circular
imports"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
