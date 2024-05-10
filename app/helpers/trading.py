"""Stores the logic for trading in a centralized location"""

from app.models import OffersModel, UserModel, INVENTORY_SIZE

def check_positive_ints_list(lst: list) -> bool:
    """Check if a list contains only positive integers"""

    for item in lst:
        if not isinstance(item, int) or item < 0:
            return False

    return True

def check_trade_possible(offer: OffersModel, accepting: UserModel, offering: UserModel) -> bool:
    """Check if a trade is possible between two players"""

    offering_inventory = offering.inventory.get_items()
    accepting_inventory = accepting.inventory.get_items()

    # Check if the offering user has enough to fulfill the trade
    for i, item in enumerate(offer.get_offering()):
        if offering_inventory[i] < item:
            return False

    # Check if the thread owner (accepting) has enough to fulfill the trade
    for i, item in enumerate(offer.get_wanting()):
        if accepting_inventory[i] < item:
            return False

    return True

def perform_trade(offer: OffersModel, accepting: UserModel, offering: UserModel) -> None:
    """Perform a trade between two players"""

    offering_inventory = offering.inventory.get_items()
    accepting_inventory = accepting.inventory.get_items()

    # wanting list goes from accepting user to the offering user
    # offering list goes from offering user to the accepting user
    for i in range(INVENTORY_SIZE):
        accepting_inventory[i] -= offer.get_wanting()[i]
        accepting_inventory[i] += offer.get_offering()[i]

        offering_inventory[i] += offer.get_wanting()[i]
        offering_inventory[i] -= offer.get_offering()[i]

    # Save the changes to the database
    offering.inventory.set_items(offering_inventory)
    accepting.inventory.set_items(accepting_inventory)

