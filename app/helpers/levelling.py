"""This module provides levelling helper functions for api endpoints"""

from datetime import datetime, timedelta

from flask import current_app
from app.databases import db
from app.models import UserModel
from app.helpers.loot_drops import calculate_next_level_requirements, single_loot_drop

def auto_level(user: UserModel) -> None:
    """Check if the user's level time is up and level up/down if necessary"""

    # Don't do anything if user has not started playing or still has time left
    if user.level == 0 or datetime.now() < user.level_expiry:
        return 0

    # Level until user is up to date, or until they cannot meet requirements
    while user.level_expiry < datetime.now() and user.has_required_items():
        ontimer_level_up(user)

    if user.level_expiry < datetime.now(): # cannot meet requirements
        level_down(user)

    db.session.add(user)

def ontimer_level_up(user: UserModel) -> None:
    """Successfully level up the user once because time is up. No auto loot drops.
    Starts next level from when the last one ended."""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Subtract requirements from inventory
    for i, requirement in enumerate(items_required):
        items[i] -= requirement

    # Set game attributes
    user.level_expiry += timedelta(days=1) # Level starts when the last one ended
    user.level += 1
    user.inventory.set_items_required(calculate_next_level_requirements())

    db.session.add(user.inventory)
    db.session.add(user)

def level_up(user: UserModel) -> list[int]:
    """Successfully level up the user and calculates changes"""

    items = user.inventory.get_items()
    items_required = user.inventory.get_items_required()

    # Subtract requirements from inventory
    for i, requirement in enumerate(items_required):
        items[i] -= requirement

    # Since level up was done before timer was up, perform auto loot drops for the time left
    # Make drops until cooldown is higher than time to next level expiry
    if user.loot_drop_refresh < datetime.now():
        user.loot_drop_refresh = datetime.now() # stops them from getting past drop opportunities
    if user.level_expiry > datetime.now():
        gained_values = []
        while user.loot_drop_refresh < user.level_expiry:
            # Get a drop and add it to the inventory
            drop = single_loot_drop()
            user.inventory.add_to_items(drop)
            gained_values.append(drop)

            # Increase the loot drop cooldown
            user.loot_drop_refresh += current_app.config['LOOT_DROP_TIMER']

        # Speeding up loot cooldown to next expiry
        user.loot_drop_refresh = datetime.now() + (user.loot_drop_refresh - user.level_expiry)

    # Set game attributes
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
    user.loot_drop_refresh = None

    db.session.add(user.inventory)
    db.session.add(user)





