"""This module provides levelling helper functions for api endpoints"""

from datetime import datetime, timedelta

from flask import current_app
from app.databases import db
from app.models import UserModel
from app.helpers.loot_drops import calculate_next_level_requirements, single_loot_drop

def auto_level(user: UserModel) -> None:
    """Check if the user's level time is up and level up/down if necessary"""

    # Check if user still has time
    if user.level_expiry is None or datetime.now() < user.level_expiry:
        return 0

    overtime = datetime.now() - user.level_expiry

    # If user does not meet requirements, or is more than 1 day late, level down
    if (overtime > timedelta(days=1)) or not user.has_required_items():
        level_down(user)
        return -1
    else:
        level_up(user)
        user.level_expiry = datetime.now() + timedelta(days=1) - overtime
        db.session.add(user)
        return 1

def level_up(user: UserModel) -> list[int]:
    """Successfully level up the user and calculates changes"""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Subtract requirements from inventory
    for i, requirement in enumerate(items_required):
        items[i] -= requirement

    # Perform loot drops until cooldown is higher than time to next level expiry
    gained_values = []
    while user.loot_drop_refresh < user.level_expiry:
        # Get a drop and add it to the inventory
        drop = single_loot_drop()
        user.inventory.add_to_items(drop)
        gained_values.append(drop)

        # Increase the loot drop cooldown
        user.loot_drop_refresh += current_app.config['LOOT_DROP_TIMER']

    # Speed up loot timer
    time_left = user.level_expiry - datetime.now()
    user.loot_drop_refresh -= time_left

    # Reset game attributes
    user.level_expiry = datetime.now() + timedelta(days=1)
    user.level += 1
    user.inventory.set_items_required(calculate_next_level_requirements())

    db.session.add(user.inventory)
    db.session.add(user)

    return gained_values

def level_down(user: UserModel) -> None:
    """Level down the user since time is up and calculate changes"""

    # Reset inventory
    user.inventory.set_items(single_loot_drop())
    user.inventory.set_items_required(calculate_next_level_requirements())

    # Reset user game attributes
    user.level = 0
    user.level_expiry = None
    user.loot_drop_refresh = datetime.now() + current_app.config['LOOT_DROP_TIMER']

    db.session.add(user.inventory)
    db.session.add(user)





