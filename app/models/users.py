"""Defines the users object and provides functions to get and manipulate one"""

from datetime import datetime

from app.models.inventory import InventoryModel
from app.databases import db

# pylint: disable=too-few-public-methods
class UserModel(db.Model):
    """Stores all users on the forum"""

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    # Authentication
    password_hash = db.Column(db.String(200), nullable=False)
    authentication_token = db.Column(db.String(200))
    change_password_token = db.Column(db.String(200))
    security_question = db.Column(db.String(200), nullable=False)
    security_question_answer = db.Column(db.String(200), nullable=False)

    admin = db.Column(db.Boolean(), default=False, nullable=False)

    # Game stats
    level = db.Column(db.Integer(), default=0, nullable=False)
    last_drop_collected = db.Column(db.DateTime(), nullable=True)

    # Relationships
    inventory = db.relationship("InventoryModel", backref="user", uselist=False)

    # Need to auto initialise inventory
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = InventoryModel(user_id=self.id)

    def to_json(self):
        """Return json from already-created user object"""
        json_user = {
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'createdAt': self.created_at,
            'inventory': self.inventory.to_list(),
        }
        return json_user
