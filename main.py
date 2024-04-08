"""Entry point for the flask application"""

from app import create_app

flask_app = create_app('dev')
