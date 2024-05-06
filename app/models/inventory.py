"""Defines the inventory object and provides functions to get and manipulate one"""

from app.databases import db

INVENTORY_SIZE = 10

# pylint: disable=too-few-public-methods
class InventoryModel(db.Model):
    """Represents a user's inventory, stored in the 'inventories' table in the DB"""

    __tablename__ = "inventories"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)

    # Set fields
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)

    # Inventory items by id - scalability currently not a priority
    q1 = db.Column(db.Integer(), default=0, nullable=False)
    q2 = db.Column(db.Integer(), default=0, nullable=False)
    q3 = db.Column(db.Integer(), default=0, nullable=False)
    q4 = db.Column(db.Integer(), default=0, nullable=False)
    q5 = db.Column(db.Integer(), default=0, nullable=False)
    q6 = db.Column(db.Integer(), default=0, nullable=False)
    q7 = db.Column(db.Integer(), default=0, nullable=False)
    q8 = db.Column(db.Integer(), default=0, nullable=False)
    q9 = db.Column(db.Integer(), default=0, nullable=False)
    q10 = db.Column(db.Integer(), default=0, nullable=False)

    def to_list(self):
        """Return list from already-created inventory object"""
        inventory_list = []
        for col in range(1, INVENTORY_SIZE + 1):
            inventory_list.append(getattr(self, f"q{col}"))
        return inventory_list
