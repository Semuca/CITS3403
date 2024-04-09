"""Sets up the api blueprint to be used by the app, avoiding circular imports"""

from flask import Blueprint

api_bp = Blueprint('api_bp', __name__)
