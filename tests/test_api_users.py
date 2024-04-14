"""Unit tests for thread endpoints"""

import unittest
import json

from app import create_app
from app.databases import db
from app.models import UserModel

def get_api_headers():
    """Gets basic headers for testing api requests"""
    return {
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }

class BaseApiTest(unittest.TestCase):
    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class TestLogin(BaseApiTest):
    """Tests log in endpoint - POST api/login"""

    def test_valid_login(self):
        """Tests that logging in with the right credentials returns the right token"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "password": "Password123"
        }

        # Act
        res = self.client.post("/api/login", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertIn("token", response_body, f"No token present in response {res.data}")
        self.assertEqual(user.authentication_token, response_body["token"], f"Token is not the same as the one in the db {res.data}")

    def test_invalid_password(self):
        """Tests that logging in with the wrong password returns a user not found error"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "password": "somethingElse"
        }

        # Act
        res = self.client.post("/api/login", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 404, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.authentication_token, None, f"Token should not be set in db {user.authentication_token}")

    def test_nonexistant_user(self):
        """Tests that trying to log in to a user that does not exist does not return an error"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123"
        ))
        db.session.commit()

        body = {
            "username": "FreddyFozbar",
            "password": "REVENGE"
        }

        # Act
        res = self.client.post("/api/login", headers=get_api_headers(), data=json.dumps(body))
        user1 = db.session.get(UserModel, 1)
        user2 = db.session.get(UserModel, 2)

        # Assert
        self.assertEqual(res.status_code, 404, f"Incorrect status code with message {res.data}")
        self.assertEqual(user1.authentication_token, None, f"Token should not be set in db {user1.authentication_token}")
        self.assertEqual(user2, None, f"User 2 should not be in db {user2}")

class TestCreateUser(BaseApiTest):
    """Tests create user endpoint - POST api/users"""

    def test_valid_create_user(self):
        """Tests that creating a user returns the right token"""

        # Assemble
        body = {
            "username": "PurpleGuy",
            "password": "Password123"
        }

        # Act
        res = self.client.post("/api/users", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertIn("token", response_body, f"No token present in response {res.data}")
        self.assertEqual(user.authentication_token, response_body["token"], f"Token is not the same as the one in the db {res.data}")

    def test_create_duplicate_user(self):
        """Tests that creating a user that already exists returns an error"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "password": "Password123"
        }

        # Act
        res = self.client.post("/api/users", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 403, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.authentication_token, None, f"Token should not be set in db {user.authentication_token}")

if __name__ == '__main__':
    unittest.main()
