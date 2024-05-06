"""Create and configure app"""
from flask import Flask
from app.models import UserModel
from config import config

from app.databases import db

flask_app = Flask(__name__)
flask_app.config.from_object(config.get('dev'))

# Bind sqlalchemy db to app
db.init_app(flask_app)

# Import and create dbs for models
with flask_app.app_context():
    db.create_all()

    db.session.add(UserModel(
        id=500,
        username="test",
        password_hash="1216985755", # Hash for 'password'
        security_question=1,
        security_question_answer="Test",
        admin=True
    ))
    db.session.commit()
