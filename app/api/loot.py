"""This module defines endpoints for user operations"""

from random import randint
from datetime import datetime, timedelta

from flask import make_response

from app.databases import db
from app.models import InventoryModel, UserModel, INVENTORY_SIZE
from app.helpers import authenticated_endpoint_wrapper

from .bp import api_bp

@api_bp.route('/loot', methods=['GET'])
def get_loot_drop():
    """Endpoint to let a user get a loot drop and returns the gained items"""

    def func(_data, request_user_id):
        # Find a user by that username and password hash
        queried_user = db.session.get(UserModel, request_user_id)

        if queried_user.last_drop_collected is not None and queried_user.last_drop_collected > datetime.now() - timedelta(hours=12):
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User has already collected a drop within the last 12 hours"},
                403)

        queried_user.last_drop_collected = datetime.now()

        gained_values = [] # Values the player is getting
        update_body = {} # Values the player will have after getting gained_values
        for i in range(0, INVENTORY_SIZE):
            gained_values.append(randint(0, 4)) # Get random value

            # Generate update body from gained_value added to inventory
            update_body.update({f"q{i + 1}": getattr(queried_user.inventory, f"q{i + 1}") + gained_values[i]})

        # Update the inventory
        queried_user.inventory.query.update(update_body)
        db.session.commit()

        # Return with the token
        return make_response({"items": gained_values})

    return authenticated_endpoint_wrapper(None, func)
