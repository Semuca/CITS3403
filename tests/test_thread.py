"""Unit test file for thread.py"""

import unittest
import json

from app import create_app
from app.databases import db
from app.models import UserModel, ThreadModel

class TestThreadModel(unittest.TestCase):
    """Tests thread database model"""

    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest"
        )
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add(self):
        """Tests adding a thread directly to the database"""

        # Create a new mock Thread object and save to db
        test_thread = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=234090
        )

        db.session.add(test_thread)
        db.session.commit()

        # Query for the thread in DB
        created_thread = db.session.get(ThreadModel, 1)

        # Assert that the created Thread object exists and has info
        self.assertIsNotNone(created_thread)
        self.assertEqual(created_thread.title, 'Exchange rare cards')
        self.assertEqual(created_thread.description, "looking for a green mage to improve defence.")
        self.assertEqual(created_thread.user_id, 234090)

class TestThreadApi(unittest.TestCase):
    """Tests thread api"""

    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest"
        )
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        """Gets basic headers for testing api requests"""
        return {
            'Authorization': 'Bearer ' + "authtest",
            'Accept': '*/*',
            'Content-Type': 'application/json'
        }

    def test_create(self):
        """Tests creating threads through the /api/threads endpoint"""

        # Posts multiple create thread requests
        req_body_1 = {
            "title": "hello",
            "description": "Heya new here"
        }

        req_body_2 = {
            "title": "Theory",
            "description": "Just a theory a game theory"
        }

        res_1 = self.client.post("/api/threads", headers=self.get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 201, f"Status code is wrong with message {res_1.data}")

        res_2 = self.client.post(
            "/api/threads",
            headers=self.get_api_headers(),
            data=json.dumps(req_body_2))
        self.assertEqual(res_2.status_code, 201, f"Status code is wrong with message {res_2.data}")

        # Check that threads are in the db and have info
        created_thread_1 = db.session.get(ThreadModel, 1)
        created_thread_2 = db.session.get(ThreadModel, 2)

        self.assertIsNotNone(created_thread_1, "Created thread is none in db")
        self.assertIsNotNone(created_thread_2, "Created thread is none in db")

        self.assertEqual(created_thread_1.title, "hello", "Created thread has wrong information")
        self.assertEqual(created_thread_2.description, "Just a theory a game theory", "Created thread has wrong information")
        self.assertEqual(created_thread_1.id, 1, "Created thread has wrong information")

    def test_read_many(self):
        """Tests reading many threads through the /api/threads endpoint"""

        # Create a couple of threads directly from the model
        test_thread_1 = ThreadModel(
            title='hello',
            description = "Heya new here",
            user_id=1
        )

        test_thread_2 = ThreadModel(
            title='Theory',
            description='Just a theory a game theory',
            user_id=1
        )

        db.session.add(test_thread_1)
        db.session.add(test_thread_2)
        db.session.commit()

        # Posts get request
        res = self.client.get("/api/threads", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the two threads created before are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 2, f"Data sent back is '{res.data}'")

        self.assertEqual(res_json_data[0]["title"], 'hello', f"Json data sent back is '{res_json_data[0]["title"]}'")
        self.assertEqual(res_json_data[0]["description"], 'Heya new here', f"Json data sent back is '{res_json_data[0]["description"]}'")
        self.assertEqual(res_json_data[0]["userId"], 1, f"Json data sent back is '{res_json_data[0]["userId"]}'")

        self.assertEqual(res_json_data[1]["title"], 'Theory', f"Json data sent back is '{res_json_data[1]["title"]}'")
        self.assertEqual(res_json_data[1]["description"], 'Just a theory a game theory', f"Json data sent back is '{res_json_data[1]["description"]}'")
        self.assertEqual(res_json_data[1]["userId"], 1, f"Json data sent back is '{res_json_data[1]["userId"]}'")

    def test_read_by_id(self):
        """Tests reading a thread by id through the /api/threads/{id} endpoint"""

        # Create a couple of threads directly from the model
        test_thread_1 = ThreadModel(
            title='hello',
            description = "Heya new here",
            user_id=1
        )

        test_thread_2 = ThreadModel(
            title='Theory',
            description='Just a theory a game theory',
            user_id=1
        )

        db.session.add(test_thread_1)
        db.session.add(test_thread_2)
        db.session.commit()

        # Posts get request
        res = self.client.get("/api/threads/2", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the thread is the right one
        res_json_data = json.loads(res.data)
        self.assertEqual(res_json_data["title"], 'Theory', f"Json data sent back is '{res_json_data}'")
        self.assertEqual(res_json_data["description"], 'Just a theory a game theory', f"Json data sent back is '{res_json_data}'")
        self.assertEqual(res_json_data["userId"], 1, f"Json data sent back is '{res_json_data["userId"]}'")

        # Posts a get request for the other thread
        res = self.client.get("/api/threads/1", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the thread is the right one
        res_json_data = json.loads(res.data)
        self.assertEqual(res_json_data["title"], 'hello', f"Json data sent back is '{res_json_data["title"]}'")
        self.assertEqual(res_json_data["description"], 'Heya new here', f"Json data sent back is '{res_json_data["description"]}'")
        self.assertEqual(res_json_data["userId"], 1, f"Json data sent back is '{res_json_data["userId"]}'")

if __name__ == '__main__':
    unittest.main()
