"""This module defines endpoints for user operations"""

from datetime import datetime, timedelta

from flask import current_app, make_response

from app.databases import db
from app.models import UserModel
from app.helpers import authenticated_endpoint_wrapper
from app.helpers.loot_drops import single_loot_drop
from app.helpers.levelling import level_up

from .bp import api_bp

@api_bp.route('/loot', methods=['GET'])
def get_loot_drop():
    """Endpoint to let a user get a single loot drop and returns the gained items"""

    def func(_data, request_user_id):
        # Find a user by id
        queried_user = db.session.get(UserModel, request_user_id)

        if queried_user.loot_drop_refresh is not None and queried_user.loot_drop_refresh > datetime.now():
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User has already collected a drop within the last 12 hours"},
                403)

        # Get gained values as a list
        gained_values = single_loot_drop()
        queried_user.inventory.add_to_items(gained_values)

        # Set up updated user body
        queried_user.loot_drop_refresh = datetime.now() + current_app.config['LOOT_DROP_TIMER']
        if queried_user.level_expiry is None:
            queried_user.level_expiry = datetime.now() + timedelta(days=1)

        db.session.commit()

        # Return with the items
        return make_response({"items": gained_values[0]})

    return authenticated_endpoint_wrapper(None, func)

@api_bp.route('/levelup', methods=['GET'])
def immediate_level_up():
    """Endpoint to let a user level up early"""

    def func(_data, request_user_id):
        queried_user = db.session.get(UserModel, request_user_id)

        # If cannot level up, don't change anything
        if queried_user.inventory.has_required_items() is False:
            return make_response(
                {"error": "Request validation error",
                "errorMessage": "User is not able to level up"},
                403)

        # Perform level up
        gains = level_up(queried_user)

        db.session.commit()

        # Return 200
        return make_response({"drops": gains})

    return authenticated_endpoint_wrapper(None, func)
