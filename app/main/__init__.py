"""Blueprint for the main parts of the app"""

from flask import Blueprint

main_bp = Blueprint('main', __name__)

# pylint: disable=wrong-import-position
from . import views
