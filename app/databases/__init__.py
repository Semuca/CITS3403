"""Creates and stores the databases for the flask application to avoid circular"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
