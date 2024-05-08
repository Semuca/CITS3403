"""Defines endpoints for CRUD operations with logs"""

from flask import make_response

from app.databases import db
from app.models import LogModel
from app.helpers import authenticated_endpoint_wrapper

from .bp import api_bp

@api_bp.route('/logs', methods=['GET'])
def read_many_logs():
    """Reads a list of threads from the database based on query parameters"""

    def func(*_):
        # Get a list of log objects according to parameters
        queried_logs = db.session.scalars(db.select(LogModel)).all()

        # Return query result to client
        return make_response([LogModel.to_json(t) for t in queried_logs], 200)

    return authenticated_endpoint_wrapper(None, func, needs_admin=True)
