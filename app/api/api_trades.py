"""Defines endpoints for CRUD operations with trades"""

from flask import make_response

from app.databases import db
from app.models import ThreadModel, OffersModel, UserModel, INVENTORY_SIZE
from app.helpers import authenticated_endpoint_wrapper, RequestSchemaDefinition
from app.helpers.trading import check_trade_possible, perform_trade, check_positive_ints_list
from app.helpers.levelling import auto_level

from .bp import api_bp

@api_bp.route('/threads/<int:thread_id>/offers', methods=['POST'])
def create_trade(thread_id):
    """Creates a trade object for a thread and saves it to the database"""

    def func(data, request_user_id):
        # Check that a thread with this id does exist
        # pylint: disable=duplicate-code
        if not ThreadModel.thread_exists(thread_id):
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Thread not found"},
                404)

        # Check that the user is not the creator of the thread
        thread = db.session.get(ThreadModel, thread_id)
        if thread.user_id == request_user_id:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Cannot trade with yourself"},
                403)

        # Get what the user that proposed the trade is offering and wanting
        offering_list = data['offeringList']
        wanting_list = data['wantingList']

        # Validate the offering and wanting lists
        if len(offering_list) != INVENTORY_SIZE or len(wanting_list) != INVENTORY_SIZE:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Offering and wanting lists must be same length as number of possible items"},
                400)
        if not check_positive_ints_list(offering_list) or not check_positive_ints_list(wanting_list):
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Offering and wanting lists must contain only positive integers"},
                400)

        # Create a trade object from parameters passed in
        new_trade_offer = OffersModel(
            user_id=request_user_id,
            thread_id=thread_id,
            offering_list=offering_list,
            wanting_list=wanting_list
        )

        # Save to db
        db.session.add(new_trade_offer)
        db.session.commit()

        # Return for successful creation of resource
        return make_response(new_trade_offer.to_json(), 201)

    return authenticated_endpoint_wrapper(create_offer_schema, func)

create_offer_schema: dict[str, str | RequestSchemaDefinition] = {
    "offeringList": "list",
    "wantingList": "list"
}

@api_bp.route('/threads/<int:thread_id>/offers/<int:trade_id>', methods=['POST'])
def accept_trade(thread_id, trade_id):
    """Accepts a trade object for a thread and saves it to the database"""

    def func(_, request_user_id):
        # Get the thread object
        thread = db.session.get(ThreadModel, thread_id)
        if thread is None:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Thread not found"},
                404)
        # Make sure the accepting user is the one who created the thread
        if thread.user_id != request_user_id:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Only the creator of the thread can accept trades"},
                403)

        # Get the trade object
        trade = db.session.get(OffersModel, trade_id)
        if trade is None:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Trade not found"},
                404)
        # Make sure the trade is for the correct thread
        if trade.thread_id != thread_id:
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Trade not for this thread"},
                403)

        # Checks if time is up for either user and performs auto level ups/downs if necessary
        queried_user = db.session.get(UserModel, request_user_id)
        queried_trade_proposer = trade.user
        auto_level(queried_user)
        auto_level(queried_trade_proposer)

        # Update the relevant users' inventories
        if not check_trade_possible(trade, thread.user, trade.user):
            return make_response(
                {"error": "Request validation error",
                 "errorMessage": "Trade not possible"},
                400)
        perform_trade(trade, thread.user, trade.user)
        db.session.commit()

        # Return for successful updated of resource
        return make_response("Update successful", 204)

    return authenticated_endpoint_wrapper(None, func)
