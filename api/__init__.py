"""This module imports all apis needed for the application"""

from flask import Blueprint

bp = Blueprint('api', __name__)

#pylint: disable=wrong-import-position
from api import login
