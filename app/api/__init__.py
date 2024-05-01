"""This module sets up the api blueprint to be used by the app"""

from .bp import api_bp
from . import comments, login, logs, threads, users
