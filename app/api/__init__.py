"""This module sets up the api blueprint to be used by the app"""

from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)

# pylint: disable=wrong-import-position
from . import login, threads
