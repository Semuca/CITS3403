"""This module provides levelling helper functions for api endpoints"""

from datetime import datetime
from flask import current_app

from app.databases import db
from app.models import UserModel
from app.helpers.loot_drops import calculate_next_level_requirements, calculate_loot_drops

def auto_level(user: UserModel) -> None:
    """Check if the user's level time is up and level up/down if necessary"""

    if user.level_expiry is not None and datetime.now() > user.level_expiry:
        if user.has_required_items():
            level_up(user)
            return 1
        else:
            level_down(user)
            return -1
    return 0

def level_up(user: UserModel) -> None:
    """Successfully level up the user and calculates changes"""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Change inventory based on requirements
    for i, requirement in enumerate(items_required):
        items[i] -= requirement
    user.inventory.set_items(items)
    user.inventory.set_items_required(calculate_next_level_requirements())

    # Work out what time is left on the level
    if datetime.now() < user.level_expiry:
        time_left = user.level_expiry - datetime.now()
    else:
        time_left = None

    # Reset user game attributes based on time left
    user.level += 1
    user.set_level_expiry()
    user.set_loot_drop_refresh(time_left=time_left)

    db.session.add(user.inventory)
    db.session.add(user)

def level_down(user: UserModel) -> None:
    """Level down the user since time is up and calculate changes"""

    # Reset inventory
    user.inventory.set_items(calculate_loot_drops(1)[0])
    user.inventory.set_items_required(calculate_next_level_requirements())

    # Reset user game attributes
    user.level = 0
    user.level_expiry = None
    user.set_loot_drop_refresh()

    db.session.add(user.inventory)
    db.session.add(user)





