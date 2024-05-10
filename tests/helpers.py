
import unittest

from app import create_app
from app.databases import db

class BaseApiTest(unittest.TestCase):
    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # create all tables in the db
        db.create_all()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

def get_api_headers():
    """Gets basic headers for testing api requests"""
    return {
        'Authorization': 'Bearer ' + "authtest",
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }
