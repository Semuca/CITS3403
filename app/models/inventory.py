"""Defines the inventory object and provides functions to get and manipulate one"""

import json

from app.databases import db
from app.helpers import calculate_loot_drops, calculate_next_level_requirements

INVENTORY_SIZE = 10

# pylint: disable=too-few-public-methods
class InventoryModel(db.Model):
    """Represents a user's inventory, stored in the 'inventories' table in the DB"""

    __tablename__ = "inventories"

    # Auto-initialised fields
    id = db.Column(db.Integer(), primary_key=True)

    # Set fields
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    items = db.Column(db.Text(), nullable=False)
    items_required = db.Column(db.Text(), nullable=False)

    # Need to store lists as json in the database
    def __init__(self, user_id):
        self.user_id = user_id
        self.set_items(calculate_loot_drops(1)[0])
        self.set_items_required(calculate_next_level_requirements())

    def save(self):
        """Commit this inventory to the database"""
        db.session.add(self)
        db.session.commit()

    def set_items(self, items_list: list[int]) -> None:
        """Stores the list of items using json in the database"""
        self.items = json.dumps(items_list)

    def get_items(self) -> list[int]:
        """Returns the list of items from the database from json"""
        return json.loads(self.items)

    def add_to_items(self, new_items_list: list[int]) -> None:
        """Adds the new items to the existing items in the database"""
        items = self.get_items()
        for col in range(INVENTORY_SIZE):
            items[col] += new_items_list[col]
        self.set_items(items)

    def set_items_required(self, items_required_list: list[int]) -> None:
        """Stores the list of required items using json in the database"""
        self.items_required = json.dumps(items_required_list)

    def get_items_required(self) -> list[int]:
        """Returns the list of required items from the database from json"""
        return json.loads(self.items_required)

    def has_required_items(self) -> bool:
        """Returns true iff the user has all the items needed to level up"""
        items = self.get_items()
        required_items = self.get_items_required()

        for i, requirement in enumerate(required_items):
            if items[i] < requirement:
                return False
        return True
