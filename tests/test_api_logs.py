"""Unit tests for thread endpoints"""

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

class TestReadMany(BaseApiTest):
    """Tests logs read-many endpoint - GET api/logs"""

    def setUp(self):
        super().setUp()

        # Create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            admin=True
        )
        db.session.add(test_user)

    def tearDown(self):
        super().tearDown()

    def test_valid_create(self):
        """Tests that logs can be read from the endpoint"""

        # Posts a couple of create thread requests
        req_body_1 = {
            "title": "hello",
            "description": "Heya new here"
        }
        req_body_2 = {
            "title": "Theory",
            "description": "Just a theory a game theory"
        }

        # Act
        thread_response_1 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_1))
        thread_response_2 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_2))

        response = self.client.get("/api/logs", headers=get_api_headers())

        # Assert
        self.assertEqual(response.status_code, 200, f"Status code is wrong with message {response.data}")
        response_body = json.loads(response.data)

        self.assertEqual(len(response_body), 2, "Response body has too many logs")
        self.assertDictEqual(response_body[0],
                             {'id': 1,
                              'userId': 1,
                              'url': '/api/threads?',
                              'requestBody': req_body_1,
                              'responseCode': thread_response_1.status_code,
                              'errorResponseBody': None,
                              'createdAt': response_body[0]['createdAt']},
                             "Log 1 is incorrect")

        self.assertDictEqual(response_body[1],
                             {'id': 2,
                              'userId': 1,
                              'url': '/api/threads?',
                              'requestBody': req_body_2,
                              'responseCode': thread_response_2.status_code,
                              'errorResponseBody': None,
                              'createdAt': response_body[1]['createdAt']},
                             "Log 1 is incorrect")



if __name__ == '__main__':
    unittest.main()
