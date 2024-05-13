"""Defines the users object and provides functions to get and manipulate one"""

from datetime import datetime, timezone

from app.models.inventory import InventoryModel
from app.databases import db

INVENTORY_CATEGORIES = ["Boar", "Cheese", "Emerald", "Feather", "Horn", "Ink", "Meat", "Mushroom", "Orb", "Scroll"]


# pylint: disable=too-few-public-methods
class UserModel(db.Model):
    """Stores all users on the forum"""

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Authentication
    password_hash = db.Column(db.String(200), nullable=False)
    authentication_token = db.Column(db.String(200))
    change_password_token = db.Column(db.String(200))
    security_question = db.Column(db.String(200), nullable=False)
    security_question_answer = db.Column(db.String(200), nullable=False)

    admin = db.Column(db.Boolean(), default=False, nullable=False)

    # Game stats
    level = db.Column(db.Integer(), default=0, nullable=False) # lv0 not playing yet, empty attributes
    _level_expiry = db.Column(db.DateTime())
    _loot_drop_refresh = db.Column(db.DateTime())

    # Relationships
    inventory = db.relationship("InventoryModel", backref="user", uselist=False)

    # Need to auto initialise inventory
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = InventoryModel(user_id=self.id)

    # need for timezone awareness when comparing against datetime.now(timezone.utc)
    # all datetime objects are stored in UTC, but accessing them will get them without timezone info, causing errors
    @property
    def level_expiry(self) -> datetime | None:
        """Property wrapper for level expiry time with the timezone info field set to UTC"""
        return self._level_expiry.replace(tzinfo=timezone.utc) if self._level_expiry else None

    @level_expiry.setter
    def level_expiry(self, value: datetime) -> None:
        """Set the level expiry time through the wrapper"""
        self._level_expiry = value

    @property
    def loot_drop_refresh(self):
        """Property wrapper for loot drop refresh time with the timezone info field set to UTC"""
        return self._loot_drop_refresh.replace(tzinfo=timezone.utc) if self._loot_drop_refresh else None

    @loot_drop_refresh.setter
    def loot_drop_refresh(self, value: datetime):
        """Set the loot drop refresh time through the wrapper"""
        self._loot_drop_refresh = value

    def to_json(self):
        """Return json from already-created user object"""
        json_user = {
            'id': self.id,
            'username': self.username,
            'description': self.description,
            'createdAt': self.created_at,
            'inventory': self.inventory.get_items(),
            'levelExpiry': self.level_expiry,
            'lootDropRefresh': self.loot_drop_refresh,
        }
        return json_user
