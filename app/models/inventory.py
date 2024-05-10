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
    q1_required = db.Column(db.Integer(), default=0, nullable=False)

    q2 = db.Column(db.Integer(), default=0, nullable=False)
    q2_required = db.Column(db.Integer(), default=0, nullable=False)

    q3 = db.Column(db.Integer(), default=0, nullable=False)
    q3_required = db.Column(db.Integer(), default=0, nullable=False)

    q4 = db.Column(db.Integer(), default=0, nullable=False)
    q4_required = db.Column(db.Integer(), default=0, nullable=False)

    q5 = db.Column(db.Integer(), default=0, nullable=False)
    q5_required = db.Column(db.Integer(), default=0, nullable=False)

    q6 = db.Column(db.Integer(), default=0, nullable=False)
    q6_required = db.Column(db.Integer(), default=0, nullable=False)

    q7 = db.Column(db.Integer(), default=0, nullable=False)
    q7_required = db.Column(db.Integer(), default=0, nullable=False)

    q8 = db.Column(db.Integer(), default=0, nullable=False)
    q8_required = db.Column(db.Integer(), default=0, nullable=False)

    q9 = db.Column(db.Integer(), default=0, nullable=False)
    q9_required = db.Column(db.Integer(), default=0, nullable=False)

    q10 = db.Column(db.Integer(), default=0, nullable=False)
    q10_required = db.Column(db.Integer(), default=0, nullable=False)

    def to_list(self) -> list[int]:
        """Return list from already-created inventory object"""
        inventory_list = []
        for col in range(INVENTORY_SIZE):
            inventory_list.append(self.get_item_by_index(col))
        return inventory_list

    def required_to_list(self) -> list[int]:
        """Return list of required inventory objects for levelling up"""
        inventory_list = []
        for col in range(INVENTORY_SIZE):
            inventory_list.append(self.get_requirement_by_index(col))
        return inventory_list

    def has_required_items(self) -> bool:
        """Returns true iff the user has all the items needed to level up"""

        for col in range(INVENTORY_SIZE):
            if self.get_item_by_index(col) < self.get_requirement_by_index(col):
                return False

        return True

    def get_item_by_index(self, item_number: int):
        """Get inventory item by item_number between 0 and INVENTORY_SIZE"""

        return getattr(self, f"q{item_number + 1}")

    def get_requirement_by_index(self, item_number: int):
        """Get inventory requirement by item_number between 0 and INVENTORY_SIZE"""

        return getattr(self, f"q{item_number + 1}_required")
