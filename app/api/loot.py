"""This module defines endpoints for user operations"""

from datetime import datetime, timedelta

from flask import make_response

from app.databases import db
from app.models import UserModel
from app.helpers import authenticated_endpoint_wrapper, calculate_loot_drops, calculate_next_level_requirements, create_inventory_update_body

from .bp import api_bp

@api_bp.route('/loot', methods=['GET'])
def get_loot_drop():
    """Endpoint to let a user get a loot drop and returns the gained items"""

    def func(_data, request_user_id):
        # Find a user by id
        queried_user = db.session.get(UserModel, request_user_id)

        if queried_user.loot_drop_refresh is not None and queried_user.loot_drop_refresh > datetime.now():
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User has already collected a drop within the last 12 hours"},
                403)

        # Get gained values as a list
        gained_values = calculate_loot_drops(1)

        # Get the updated inventory body by converting the gained_values
        inventory_update_body = create_inventory_update_body(queried_user, gained_values)

        # Set up updated user body
        user_update_body = {"loot_drop_refresh": datetime.now() + timedelta(hours=12)}
        # If the user does not have a level expiry set, start on collecting a drop
        if queried_user.level_expiry is None:
            user_update_body["level_expiry"] = datetime.now() + timedelta(days=1)

        # Update the user and inventory databases
        queried_user.query.update(user_update_body)
        queried_user.inventory.query.update(inventory_update_body)
        db.session.commit()

        # Return with the items
        return make_response({"items": gained_values[0]})

    return authenticated_endpoint_wrapper(None, func)

@api_bp.route('/levelup', methods=['GET'])
def level_up():
    """Endpoint to let a user level up early"""

    def func(_data, request_user_id):
        # Find a user by id
        queried_user = db.session.get(UserModel, request_user_id)

        if queried_user.inventory.has_required_items() is False:
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User is not able to level up"},
                403)

        # Calculate successive loot drop points and count how many occur
        next_loot_drop_point = queried_user.loot_drop_refresh

        drops_count = 0
        while next_loot_drop_point < queried_user.level_expiry:
            next_loot_drop_point += timedelta(hours=12)
            drops_count += 1

        # Calculate remaining time until next loot drop from this speedup
        loot_drop_time_remaining = next_loot_drop_point - queried_user.level_expiry

        # Generate loot drops and new requirements
        drops = calculate_loot_drops(drops_count)
        inventory_update_body = create_inventory_update_body(queried_user, drops, calculate_next_level_requirements())

        # Update the user database
        # Next loot drop is in now + 12 hours - the time that has been saved
        # Next level expiry is in one day
        queried_user.query.update({"level": queried_user.level + 1,
                                   "loot_drop_refresh": datetime.now() + loot_drop_time_remaining,
                                   "level_expiry": datetime.now() + timedelta(days=1)})

        # Update the inventory database
        queried_user.inventory.query.update(inventory_update_body)
        db.session.commit()

        # Return 200
        return make_response({"drops": drops})

    return authenticated_endpoint_wrapper(None, func)
