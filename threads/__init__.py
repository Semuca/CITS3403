"""This module imports the threads api and relevant functions"""

from flask import Blueprint

threads_bp = Blueprint('threads_api', __name__)

#pylint: disable=wrong-import-position
from threads import routes