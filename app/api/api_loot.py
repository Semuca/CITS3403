"""This module defines endpoints for loot and level up operations"""

from datetime import datetime, timezone

from flask import current_app, make_response

from app.databases import db
from app.models import UserModel
from app.helpers import authenticated_endpoint_wrapper
from app.helpers.loot_drops import single_loot_drop
from app.helpers.levelling import manual_level_up, auto_level

from .bp import api_bp

@api_bp.route('/loot', methods=['GET'])
def get_loot_drop():
    """Endpoint to let a user get a single loot drop and returns the gained items"""

    def func(_data, request_user_id):
        # Find a user by id
        queried_user = db.session.get(UserModel, request_user_id)

        # Checks if time is up and performs auto level ups/downs if necessary
        auto_level(queried_user)

        # if cooldown finish is in the future, return error
        if queried_user.level != 0 and queried_user.loot_drop_refresh > datetime.now(timezone.utc):
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User has already collected a drop within the last 12 hours"},
                403)

        # Get gained values as a list
        gained_values = single_loot_drop()
        queried_user.inventory.add_to_items(gained_values)

        # If this is the first drop, start the level timer and put the user in the first level
        if queried_user.level == 0:
            queried_user.level = 1
            queried_user.level_expiry = datetime.now(timezone.utc) + current_app.config['LEVEL_EXPIRY_TIMER']
            queried_user.inventory.set_items_required(single_loot_drop())

        # Reset the loot drop timer
        queried_user.loot_drop_refresh = datetime.now(timezone.utc) + current_app.config['LOOT_DROP_TIMER']

        db.session.commit()

        # Return with the items
        return make_response({"items": gained_values})

    return authenticated_endpoint_wrapper(None, func)

@api_bp.route('/levelup', methods=['GET'])
def immediate_level_up():
    """Endpoint to let a user level up early"""

    def func(_data, request_user_id):
        queried_user = db.session.get(UserModel, request_user_id)

        # Checks if time is up and performs auto level ups/downs if necessary
        auto_level(queried_user)

        # If user hasn't collected a drop yet (hasn't started playing), return error
        if queried_user.level == 0:
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User has not collected a first drop yet"},
                403)
        # If cannot level up, don't change anything
        if queried_user.inventory.has_required_items() is False:
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User does not have the resources to level up"},
                403)

        # Perform level up
        gains = manual_level_up(queried_user)

        db.session.commit()

        # Return 200
        return make_response({"drops": gains})

    return authenticated_endpoint_wrapper(None, func)
