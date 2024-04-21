"""Unit tests for users endpoints"""

import unittest
import json

from app import create_app
from app.databases import db
from app.models import UserModel

from .helpers import get_api_headers

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
    def setUp(self):
        super().setUp()

        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            security_question=3,
            security_question_answer="Purple"
        ))
        db.session.commit()

    def test_valid_login(self):
        """Tests that logging in with the right credentials returns the right token"""

        # Assemble
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
        """Tests that trying to log in to a user that does not exist returns an error"""

        # Assemble
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
            "password": "Password123",
            "securityQuestion": 1,
            "securityQuestionAnswer": "Purple"
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
            password_hash="Password123",
            security_question=3,
            security_question_answer="idk"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "password": "Password123",
            "securityQuestion": 1,
            "securityQuestionAnswer": "Purple"
        }

        # Act
        res = self.client.post("/api/users", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 403, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.authentication_token, None, f"Token should not be set in db {user.authentication_token}")

class TestChangePasswordWithQuestion(BaseApiTest):
    """Tests change password with questions - POST api/login/questions"""

    def test_valid_change_password(self):
        """Tests that getting a password change token returns the right token"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "securityQuestionAnswer": "Purple"
        }

        # Act
        res = self.client.post("/api/login/questions", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertIn("token", response_body, f"No token present in response {res.data}")
        self.assertEqual(user.change_password_token, response_body["token"], f"Token is not the same as the one in the db {res.data}")

    def test_incorrect_change_password(self):
        """Tests that changing a password incorrectly results in an error"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "username": "PurpleGuy",
            "securityQuestionAnswer": "somethingRandom"
        }

        # Act
        res = self.client.post("/api/login/questions", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 404, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.change_password_token, None, f"Token should not be set in db {user.change_password_token}")

class TestChangePasswordUnauthenticated(BaseApiTest):
    """Tests change password with questions - POST api/login/password"""

    def test_valid_change_password(self):
        """Tests that getting a password change token returns the right token"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            change_password_token="token",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "password": "newPassword",
            "changePasswordToken": "token",
        }

        # Act
        res = self.client.post("/api/login/password", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertIn("token", response_body, f"No token present in response {res.data}")
        self.assertEqual(user.authentication_token, response_body["token"], f"Token is not the same as the one in the db {res.data}")
        self.assertEqual(user.change_password_token, None, f"Change password token should not be set in db {user}")

    def test_incorrect_change_password(self):
        """Tests that changing a password incorrectly results in an error"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "password": "newPassword",
            "changePasswordToken": "unknown",
        }

        # Act
        res = self.client.post("/api/login/password", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 404, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.authentication_token, None, f"Token is not the same as the one in the db {res.data}")
        self.assertEqual(user.change_password_token, None, f"Change password token should not be set in db {user}")

class TestChangeQuestionsAuthenticated(BaseApiTest):
    """Tests change questions while authenticated - POST api/users/questions"""

    def test_valid_change_questions(self):
        """Tests that changing security questions returns correctly"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            authentication_token="authtest",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "securityQuestion": 4,
            "securityQuestionAnswer": "Nine",
        }

        # Act
        res = self.client.post("/api/users/questions", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        self.assertEqual(user.security_question, str(body["securityQuestion"]), f"Security question is not the same as the one in the db {body}")
        self.assertEqual(user.security_question_answer, body["securityQuestionAnswer"],
                         f"Security question answer is not the same as the one in the db {body}")

class TestChangePasswordAuthenticated(BaseApiTest):
    """Tests change password while authenticated - POST api/users/password"""

    def test_valid_change_password(self):
        """Tests that changing password returns correctly"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash="Password123",
            authentication_token="authtest",
            security_question=1,
            security_question_answer="Purple"
        ))
        db.session.commit()

        body = {
            "password": "newPassword",
        }

        # Act
        res = self.client.post("/api/users/password", headers=get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        self.assertEqual(user.password_hash, body["password"], f"Security question is not the same as the one in the db {body}")

if __name__ == '__main__':
    unittest.main()
