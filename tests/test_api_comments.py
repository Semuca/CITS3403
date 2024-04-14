"""Unit tests for comment endpoints"""

import unittest
import json

from app import create_app
from app.databases import db
from app.models import UserModel, ThreadModel, CommentModel

def get_api_headers():
    """Gets basic headers for testing api requests"""
    return {
        'Authorization': 'Bearer ' + "authtest",
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

class TestCreate(BaseApiTest):
    """Tests threads create endpoint - POST api/threads/{thread_id}/comments"""

    def setUp(self):
        super().setUp()

        # Create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest"
        )
        db.session.add(test_user)

        # Create a new thread directly with the database
        test_thread = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        db.session.add(test_thread)

        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_valid_create(self):
        """Tests that comments can be created from the endpoint"""

        # Posts a couple of create comment requests
        req_body_1 = {
            "data": "Do you have any with rank above B I will trade"
        }
        res_1 = self.client.post("/api/threads/1/comments", headers=get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 201, f"Status code is wrong with message {res_1.data}")

        req_body_2 = {
            "data": "If u like anything in my inventory I am down to trade"
        }
        res_2 = self.client.post("/api/threads/1/comments", headers=get_api_headers(), data=json.dumps(req_body_2))
        self.assertEqual(res_2.status_code, 201, f"Status code is wrong with message {res_2.data}")

        # Check that comments are in the db and have info
        created_comment_1 = db.session.get(CommentModel, 1)
        created_comment_2 = db.session.get(CommentModel, 2)

        self.assertIsNotNone(created_comment_1)
        self.assertIsNotNone(created_comment_2)

        self.assertEqual(created_comment_1.data, "Do you have any with rank above B I will trade")
        self.assertEqual(created_comment_1.user_id, 1)
        self.assertEqual(created_comment_1.thread_id, 1)

        self.assertEqual(created_comment_2.data, "If u like anything in my inventory I am down to trade")
        self.assertEqual(created_comment_2.user_id, 1)
        self.assertEqual(created_comment_2.thread_id, 1)

        # Check that the comments can be properly accessed through the thread model
        test_thread = db.session.get(ThreadModel, 1)

        self.assertEqual(len(test_thread.children), 2)
        self.assertEqual(test_thread.children[0].data, "Do you have any with rank above B I will trade")
        self.assertEqual(test_thread.children[1].data, "If u like anything in my inventory I am down to trade")

class TestReadMany(BaseApiTest):
    """Tests comments read many endpoint - GET api/threads/{thread_id}/children"""

    def setUp(self):
        super().setUp()

        # Create new user directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest"
        )
        db.session.add(test_user)

        # Create a couple of threads directly with the database
        test_thread_1 = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        test_thread_2 = ThreadModel(
            title='hello',
            description="Heya new here",
            user_id=1
        )
        db.session.add(test_thread_1)
        db.session.add(test_thread_2)

        # Create a couple of comments directly with the database
        test_comment_1 = CommentModel(
            data="Do you have any with rank above B? I will trade",
            thread_id=1,
            user_id=1
        )
        test_comment_2 = CommentModel(
            data="If u like anything in my inventory I'm down to trade",
            thread_id=1,
            user_id=1
        )
        db.session.add(test_comment_1)
        db.session.add(test_comment_2)

    def tearDown(self):
        super().tearDown()

    def test_valid_read_many(self):
        """Tests that comments can be received from the endpoint"""

        # Post a get request for all the comments in the test thread with two comments
        res = self.client.get("/api/threads/1/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the two comments created before are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 2, f"Data sent back is '{res.data}'")

        self.assertEqual(res_json_data[0]["data"], 'Do you have any with rank above B? I will trade', f"Json data sent back is '{res_json_data[0]["data"]}'")
        self.assertEqual(res_json_data[0]["threadId"], 1, f"Json data sent back is '{res_json_data[0]["threadId"]}'")
        self.assertEqual(res_json_data[0]["userId"], 1, f"Json data sent back is '{res_json_data[0]["userId"]}'")

        self.assertEqual(res_json_data[1]["data"], "If u like anything in my inventory I'm down to trade", f"Json data sent back is '{res_json_data[1]["data"]}'")
        self.assertEqual(res_json_data[1]["threadId"], 1, f"Json data sent back is '{res_json_data[1]["threadId"]}'")
        self.assertEqual(res_json_data[1]["userId"], 1, f"Json data sent back is '{res_json_data[1]["userId"]}'")

    def test_get_from_no_comments_thread(self):
        """Tests that getting with no comments gets an empty list"""

        # Post a get request for all the comments in the test thread with no comments
        res = self.client.get("/api/threads/2/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 0, f"Data sent back is '{res.data}'")
