"""This module provides levelling helper functions for api endpoints"""

from datetime import datetime, timedelta, timezone

from flask import current_app
from app.databases import db
from app.models import UserModel, INVENTORY_SIZE
from app.helpers.loot_drops import calculate_next_level_requirements, single_loot_drop

def auto_level(user: UserModel) -> None:
    """Check if the user's level time is up and level up/down if necessary"""

    # Don't do anything if user has not started playing or still has time left
    if user.level == 0 or datetime.now(timezone.utc) < user.level_expiry:
        return

    # Level until user is up to date, or until they cannot meet requirements
    while user.level_expiry < datetime.now(timezone.utc) and user.inventory.has_required_items():
        auto_level_up(user)

    if user.level_expiry < datetime.now(timezone.utc): # cannot meet requirements
        level_down(user)

    db.session.add(user)
    db.session.commit()

def auto_level_up(user: UserModel) -> None:
    """Successfully level up the user once because time is up. No auto loot drops.
    Starts next level from when the last one ended."""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Subtract requirements from inventory
    for i, requirement in enumerate(items_required):
        items[i] -= requirement

    # Set game attributes
    user.level_expiry += current_app.config['LEVEL_EXPIRY_TIMER'] # Level starts when the last one ended
    user.level += 1
    user.inventory.set_items(items)
    user.inventory.set_items_required(calculate_next_level_requirements())

    db.session.add(user.inventory)
    db.session.add(user)

def manual_level_up(user: UserModel) -> list[list[int]]:
    """Successfully level up the user before time is up.
    Auto loot drops are calculated for the time left, and next level starts now.
    Returns the list of drops lists."""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Subtract requirements from inventory
    for i, requirement in enumerate(items_required):
        items[i] -= requirement
    user.inventory.set_items(items)

    # Set loot drop cooldown to now if it's in the past, to stop users from getting past drops
    user.loot_drop_refresh = max(user.loot_drop_refresh, datetime.now(timezone.utc))

    # Perform auto loot drops for the time left, until cooldown is higher than time to next level
    gained_values = []
    while user.loot_drop_refresh < user.level_expiry:
        # Get a drop and add it to the inventory
        drop = single_loot_drop()
        user.inventory.add_to_items(drop)
        gained_values.append(drop)

        # Increase the loot drop cooldown
        user.loot_drop_refresh += current_app.config['LOOT_DROP_TIMER']

    # Speed up loot cooldown to next expiry
    user.loot_drop_refresh = datetime.now(timezone.utc) + (user.loot_drop_refresh - user.level_expiry)

    # Set game attributes
    user.level_expiry = datetime.now(timezone.utc) + current_app.config['LEVEL_EXPIRY_TIMER']
    user.level += 1
    user.inventory.set_items_required(calculate_next_level_requirements())

    db.session.add(user.inventory)
    db.session.add(user)
    db.session.commit()

    return gained_values

def level_down(user: UserModel) -> None:
    """Level down the user since time is up and calculate changes"""

    # Reset inventory
    user.inventory.set_items([0 for x in range(INVENTORY_SIZE)])
    user.inventory.set_items_required([0 for x in range(INVENTORY_SIZE)])

    # Reset user game attributes
    user.level = 0
    user.level_expiry = None
    user.loot_drop_refresh = None

    db.session.add(user.inventory)
    db.session.add(user)
