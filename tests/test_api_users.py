"""Unit tests for users endpoints"""

import unittest
import json
import hashlib

from app.databases import db
from app.models import UserModel

from .helpers import BaseApiTest

class TestGetUser(BaseApiTest):
    """Tests get user endpoint - GET api/users"""

    def test_valid_get_user(self):
        """Tests that getting a user returns the right user"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            description="I'm the man behind the slaughter",
            password_hash="Password123",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="idk"
        ))
        db.session.commit()

        # Act
        res = self.client.get("/api/users", headers=self.get_api_headers())
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertEqual(response_body["id"], user.id, f"Id is not the same as the one in the db {res.data}")
        self.assertEqual(response_body["username"], user.username, f"Username is not the same as the one in the db {res.data}")
        self.assertEqual(response_body["description"], user.description, f"Description is not the same as the one in the db {res.data}")

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
        res = self.client.post("/api/users", headers=self.get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        response_body = json.loads(res.data)
        self.assertIn("token", response_body, f"No token present in response {res.data}")
        self.assertEqual(user.authentication_token, response_body["token"], f"Token is not the same as the one in the db {res.data}")
        self.assertEqual(user.inventory.get_items(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], f"Wrong inventory in db {res.data}")
        self.assertEqual(user.level, 0, f"Wrong level in db {res.data}")


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
        res = self.client.post("/api/users", headers=self.get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 403, f"Incorrect status code with message {res.data}")
        self.assertEqual(user.authentication_token, None, f"Token should not be set in db {user.authentication_token}")

class TestEditUser(BaseApiTest):
    """Tests change questions while authenticated - PUT api/users"""

    def test_valid_change_questions(self):
        """Tests that changing security questions returns correctly"""

        # Assemble
        hashed_password = hashlib.sha256("Password123".encode()).hexdigest()
        hashed_sec_answer = hashlib.sha256("Purple".encode()).hexdigest()
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash=hashed_password,
            description="desc",
            authentication_token="authtest",
            security_question=1,
            security_question_answer=hashed_sec_answer
        ))
        db.session.commit()

        body = {
            "securityQuestion": 4,
            "securityQuestionAnswer": "Nine",
        }

        # Act
        res = self.client.put("/api/users", headers=self.get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        self.assertEqual(user.security_question, str(body["securityQuestion"]), f"Security question is not the same as the one in the db {body}")
        self.assertEqual(user.security_question_answer, hashlib.sha256(body["securityQuestionAnswer"].encode()).hexdigest(),
                         f"Security question answer is not the same as the one in the db {body}")
        self.assertEqual(user.description, "desc", f"Users description should not have changed {body}")

    def test_valid_change_password(self):
        """Tests that changing password returns correctly"""

        # Assemble
        hashed_password = hashlib.sha256("Password123".encode()).hexdigest()
        hashed_sec_answer = hashlib.sha256("Purple".encode()).hexdigest()
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash=hashed_password,
            authentication_token="authtest",
            security_question=1,
            security_question_answer=hashed_sec_answer
        ))
        db.session.commit()

        body = {
            "password": "newPassword",
        }

        # Act
        res = self.client.put("/api/users", headers=self.get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        self.assertEqual(user.password_hash, hashlib.sha256(body["password"].encode()).hexdigest(), f"Password hash is not the same as the one in the db {body}")

    def test_valid_change_description(self):
        """Tests that changing description returns correctly"""

        # Assemble
        hashed_password = hashlib.sha256("Password123".encode()).hexdigest()
        hashed_sec_answer = hashlib.sha256("Purple".encode()).hexdigest()
        db.session.add(UserModel(
            username="PurpleGuy",
            password_hash=hashed_password,
            description="desc",
            authentication_token="authtest",
            security_question=1,
            security_question_answer=hashed_sec_answer
        ))
        db.session.commit()

        body = {
            "description": "new description",
        }

        # Act
        res = self.client.put("/api/users", headers=self.get_api_headers(), data=json.dumps(body))
        user = db.session.get(UserModel, 1)

        # Assert
        self.assertEqual(res.status_code, 200, f"Incorrect status code with message {res.data}")

        self.assertEqual(user.description, body["description"], f"Description is not the same as the one in the db {body}")

if __name__ == '__main__':
    unittest.main()
