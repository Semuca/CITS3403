"""Stores the logic for loot drops in a centralized location"""

from random import randint, shuffle

from app.models import INVENTORY_SIZE
from app.models import UserModel


def calculate_loot_drops(drop_count: int) -> list[list[int]]:
    """Calculate a loot drop as a list of 'drops' loot drops"""

    drops = [[0 for x in range(INVENTORY_SIZE)] for y in range(drop_count)] # Drops the player is getting

    for drop in drops:
        for i, _item in enumerate(drop):
            drop[i] += randint(0, 4) # Get random value

    return drops

def calculate_next_level_requirements() -> list[int]:
    """Calculate next level requirements as a list"""

    # Inventory as a list
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

def create_inventory_update_body(user: UserModel, drops: list[list[int]] = None, new_requirements: list[int] = None) -> dict[str, int]:
    """Create a dictionary based off arrays to update the inventory"""

    gained_values = [0 for x in range(INVENTORY_SIZE)]
    if drops is not None:
        for drop in drops:
            for i in range(INVENTORY_SIZE):
                gained_values[i] += drop[i]

    update_body: dict[str, int] = {}
    for i in range(INVENTORY_SIZE):
        update_body.update({f"q{i + 1}": user.inventory.get_item_by_index(i) + gained_values[i]})
        if new_requirements is not None and len(new_requirements) == INVENTORY_SIZE:
            update_body.update({f"q{i + 1}_required": new_requirements[i]})

    return update_body
