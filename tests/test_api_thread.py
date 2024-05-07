"""Unit tests for thread endpoints"""

import unittest
import json

from app.databases import db
from app.models import UserModel, ThreadModel

from .helpers import BaseApiTest, get_api_headers

class TestCreate(BaseApiTest):
    """Tests threads create endpoint - POST api/threads"""

    def setUp(self):
        super().setUp()

        # Create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user)

    def test_valid_create(self):
        """Tests that threads can be created from the endpoint"""

        # Posts a couple of create thread requests
        req_body_1 = {
            "title": "hello",
            "description": "Heya new here"
        }
        res_1 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 201, f"Status code is wrong with message {res_1.data}")

        req_body_2 = {
            "title": "Theory",
            "description": "Just a theory a game theory"
        }
        res_2 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_2))
        self.assertEqual(res_2.status_code, 201, f"Status code is wrong with message {res_2.data}")

        # Check that threads are in the db and have info
        created_thread_1 = db.session.get(ThreadModel, 1)
        created_thread_2 = db.session.get(ThreadModel, 2)

        self.assertIsNotNone(created_thread_1)
        self.assertIsNotNone(created_thread_2)

        self.assertEqual(created_thread_1.title, "hello", "Created thread has wrong information")
        self.assertEqual(created_thread_1.description, "Heya new here", "Created thread has wrong information")
        self.assertEqual(created_thread_1.user_id, 1, "Created thread has wrong information")

        self.assertEqual(created_thread_2.title, "Theory", "Created thread has wrong information")
        self.assertEqual(created_thread_2.description, "Just a theory a game theory", "Created thread has wrong information")
        self.assertEqual(created_thread_2.user_id, 1, "Created thread has wrong information")

    def test_create_missing_header(self):
        """Tests that creating thread with a required header missing returns the right error"""

        # Posts a couple of bad create thread requests
        req_body_1 = {
            "title": "hello",
        }
        res_1 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 400, f"Status code is wrong with message {res_1.data}")

        req_body_2 = {
            "description": "Just a theory a game theory"
        }
        res_2 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_2))
        self.assertEqual(res_2.status_code, 400, f"Status code is wrong with message {res_2.data}")

    def test_create_too_many_headers(self):

        # Posts a bad create thread requests
        req_body_1 = {
            "title": "hello",
            "description": "Heya new here",
            "aaaaa": "AAAAA"
        }
        res_1 = self.client.post("/api/threads", headers=get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 400, f"Status code is wrong with message {res_1.data}")

class TestReadMany(BaseApiTest):
    """Tests threads read many endpoint - GET api/threads"""

    def setUp(self):
        super().setUp()

        # Create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user)

        # Create a couple of threads directly with the database to get later
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

    def test_valid_read_many(self):
        # Post a get request for all the threads
        res = self.client.get("/api/threads", headers=get_api_headers())
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

    def test_get_from_empty_database(self):
        # Empty the database
        db.session.query(ThreadModel).delete()

        # Post a get request for all the threads
        res = self.client.get("/api/threads", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that there only an empty list sent back
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 0, f"Data sent back is '{res.data}'")

    def test_get_with_pagination(self):
        # Create a sizable number more threads directly with the database
        for i in range(3, 12):
            new_thread = ThreadModel(
                title=f'thread{i}',
                description=f'description{i}',
                user_id=1
            )
            db.session.add(new_thread)
        db.session.commit()

        # Post a get request for first 8 threads
        res = self.client.get("/api/threads?page=1&perPage=8", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the first 8 threads are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 8, f"Data sent back is of length '{len(res_json_data)}'")
        self.assertEqual(res_json_data[0]["title"], 'hello', f"Json data sent back is '{res_json_data[0]["title"]}'")
        self.assertEqual(res_json_data[4]["description"], 'description5', f"Json data sent back is '{res_json_data[4]["description"]}'")
        self.assertEqual(res_json_data[7]["title"], 'thread8', f"Json data sent back is '{res_json_data[7]["title"]}'")

        # Post a get request for last 4 threads
        res = self.client.get("/api/threads?page=2&perPage=8", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the last 4 threads are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 3, f"Data sent back is of length '{len(res_json_data)}'")
        self.assertEqual(res_json_data[0]["title"], 'thread9', f"Json data sent back is '{res_json_data[0]["title"]}'")
        self.assertEqual(res_json_data[1]["description"], 'description10', f"Json data sent back is '{res_json_data[1]["description"]}'")

    def test_default_pagination(self):
        # Create a sizable number more threads directly with the database
        for i in range(3, 12):
            new_thread = ThreadModel(
                title=f'thread{i}',
                description=f'description{i}',
                user_id=1
            )
            db.session.add(new_thread)
        db.session.commit()

        # Post a get request for first 10 threads
        res = self.client.get("/api/threads", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the first 10 threads are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 10, f"Data sent back is of length '{len(res_json_data)}")
        self.assertEqual(res_json_data[0]["title"], 'hello', f"Json data sent back is '{res_json_data[0]["title"]}'")
        self.assertEqual(res_json_data[4]["description"], 'description5', f"Json data sent back is '{res_json_data[4]["description"]}'")
        self.assertEqual(res_json_data[9]["title"], 'thread10', f"Json data sent back is '{res_json_data[9]["title"]}'")

    def test_get_with_search(self):
        # Create a sizable number more threads directly with the database
        for i in range(3, 12):
            new_thread = ThreadModel(
                title=f'thread{i}',
                description=f'description{i}',
                user_id=1
            )
            db.session.add(new_thread)
        db.session.commit()

        # The endpoint curently only supports searches for the title of the threads

        # Post a get request for threads with 'thread' in the title
        res = self.client.get("/api/threads?search=thread", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the threads with 'thread' in the title are returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 9, f"Data sent back is of length '{len(res_json_data)}")
        self.assertEqual(res_json_data[0]["title"], 'thread3', f"Json data sent back is '{res_json_data[0]["title"]}'")
        self.assertEqual(res_json_data[8]["title"], 'thread11', f"Json data sent back is '{res_json_data[8]["title"]}'")

        # Post a get request for threads with '5' in the description
        res = self.client.get("/api/threads?search=5", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the thread with '5' in the title is returned with the right information
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 1, f"Data sent back is of length '{len(res_json_data)}")
        self.assertEqual(res_json_data[0]["title"], 'thread5', f"Json data sent back is '{res_json_data[0]["title"]}'")

class TestReadById(BaseApiTest):
    """Tests threads read by id endpoint - GET api/threads/{id}"""

    def setUp(self):
        super().setUp()

        # Create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user)

        # Create a couple of threads directly with the database to get later
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

    def test_get_valid_thread(self):
        """Test that threads can be received from the endpoint"""

        # Post a get request for first thread
        res = self.client.get("/api/threads/1", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the thread is the right one
        res_json_data = json.loads(res.data)
        self.assertEqual(res_json_data["title"], 'hello', f"Json data sent back is '{res_json_data["title"]}'")
        self.assertEqual(res_json_data["description"], 'Heya new here', f"Json data sent back is '{res_json_data["description"]}'")
        self.assertEqual(res_json_data["userId"], 1, f"Json data sent back is '{res_json_data["userId"]}'")

        # Post a get request for second thread
        res = self.client.get("/api/threads/2", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message '{res.data}'")

        # Check that the thread is the right one
        res_json_data = json.loads(res.data)
        self.assertEqual(res_json_data["title"], 'Theory', f"Json data sent back is '{res_json_data}'")
        self.assertEqual(res_json_data["description"], 'Just a theory a game theory', f"Json data sent back is '{res_json_data}'")
        self.assertEqual(res_json_data["userId"], 1, f"Json data sent back is '{res_json_data["userId"]}'")

    def test_get_nonexistent_thread(self):
        """Tests that getting with a nonexistent thread ids gets the right error response"""

        res_1 = self.client.get("/api/threads/3", headers=get_api_headers())
        res_2 = self.client.get("/api/threads/awawa", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 404, f"Status code is wrong with message '{res_1.data}'")
        self.assertEqual(res_2.status_code, 404, f"Status code is wrong with message '{res_2.data}'")

if __name__ == '__main__':
    unittest.main()
