"""This module sets up the api blueprint to be used by the app"""

from .bp import api_bp
from . import api_comments, api_login, api_logs, api_loot, api_threads, api_users
