"""Stores the logic for loot drops in a centralized location"""

from random import randint, shuffle

from app.models import INVENTORY_SIZE

def calculate_loot_drops(drop_count: int) -> list[list[int]]:
    """Calculate a loot drop as a list of 'drops' loot drops"""

    drops = [[0 for x in range(INVENTORY_SIZE)] for y in range(drop_count)] # Drops the player is getting

    for drop in drops:
        for i, _item in enumerate(drop):
            drop[i] += randint(0, 4) # Get random value

    return drops

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
