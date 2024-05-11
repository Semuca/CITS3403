"""Defines the trades object and provides functions to get and manipulate one"""

from datetime import datetime
import json

from app.databases import db
from app.models.inventory import INVENTORY_SIZE

# pylint: disable=too-few-public-methods
class OffersModel(db.Model):
    """Represents a single trade offer, stored in the 'offers' table in the DB"""

    __tablename__ = "offers"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)

    # Set fields
    offering = db.Column(db.Text(), nullable=False)
    wanting = db.Column(db.Text(), nullable=False)
    thread_id = db.Column(db.Integer(), db.ForeignKey("threads.id"), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = db.relationship("UserModel", backref="offers")
    thread_child_type = "offer"

    # Need to store lists as json in the database
    def __init__(self, user_id, thread_id, offering_list, wanting_list):
        self.user_id = user_id
        self.thread_id = thread_id

        if len(offering_list) != INVENTORY_SIZE or len(wanting_list) != INVENTORY_SIZE:
            raise ValueError("Offering and wanting lists must be same length as number of possible items")
        self.set_offering(offering_list)
        self.set_wanting(wanting_list)

    def to_json(self):
        """Return json from already-created trade object"""
        json_trade_offer = {
            'id': self.id,
            'childType': 'offer',
            'userId': self.user_id,
            'threadId': self.thread_id,
            'createdAt': self.created_at,
            'offering': self.get_offering(),
            'wanting': self.get_wanting(),
            'user': self.user.to_json(),
        }
        return json_trade_offer

    def set_offering(self, offering_list):
        """Stores the list of offerings using json in the database"""
        self.offering = json.dumps(offering_list)

    def get_offering(self):
        """Returns the list of offerings from the database from json"""
        return json.loads(self.offering)

    def set_wanting(self, wanting_list):
        """Stores the list of wanted items using json in the database"""
        self.wanting = json.dumps(wanting_list)

    def get_wanting(self):
        """Returns the list of wanted items from the database from json"""
        return json.loads(self.wanting)
