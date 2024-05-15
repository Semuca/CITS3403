"""Stores the logic for loot drops in a centralized location"""

from random import randint, shuffle
from flask import current_app

from app.databases import db
from app.models import INVENTORY_SIZE, UserModel

def single_loot_drop() -> list[int]:
    """Calculate a single loot drop"""
    return [randint(0, 4) for x in range(INVENTORY_SIZE)]

def perform_loot_drops(user: UserModel) -> list[int]:
    """Performs maximum possible loot drops. Default cooldown is 12 hours, default time left is 0."""

    gained_values = []
    while user.loot_drop_refresh < user.level_expiry:
        drop = single_loot_drop()
        user.inventory.add_to_items(drop)

        user.loot_drop_refresh += current_app.config['LOOT_DROP_TIMER']
        gained_values.append(drop)

    db.session.add(user.inventory)
    db.session.add(user)

    return gained_values

def calculate_next_level_requirements() -> list[int]:
    """Calculate next level requirements as a list"""

    # Store the next level up requirements in a list
    requirements = [0 for x in range(INVENTORY_SIZE)]

    # Choose 10 and 14 points to allocate
    points = randint(10, 14)

    # Choose a random value from the inventory_list only once and add a random selection to that
    points_selection = list(range(INVENTORY_SIZE))
    shuffle(points_selection)
    while points != 0:
        selected_point = points_selection.pop()

        # Select a random amount of the points left
        required_amount = min(points, randint(4, 6))

        # Allocate the required amount to a point
        requirements[selected_point] = required_amount
        points -= required_amount

    return requirements
