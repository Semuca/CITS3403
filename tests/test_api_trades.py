"""Unit tests for trade endpoints"""

import unittest
import json

from app.databases import db
from app.models import UserModel, ThreadModel, OffersModel, CommentModel

from .helpers import BaseApiTest, get_api_headers

class TestCreate(BaseApiTest):
    """Tests threads create endpoint - POST api/threads/{thread_id}/offers"""

    def setUp(self):
        super().setUp()

        # Create new users with auth token directly with the database
        test_user_1 = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_1)

        test_user_2 = UserModel(
            username="test2",
            password_hash="test",
            authentication_token="authtest2",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_2)

        test_thread_1 = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        db.session.add(test_thread_1)

        # Create a new thread directly with the database
        test_thread_2 = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=2
        )
        db.session.add(test_thread_2)

        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_valid_create(self):
        """Tests that trades can be created from the endpoint"""

        # Posts a couple of create trade requests
        req_body_1 = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res_1 = self.client.post("/api/threads/2/offers", headers=get_api_headers(), data=json.dumps(req_body_1))
        self.assertEqual(res_1.status_code, 201, f"Status code is wrong with message {res_1.data}")

        req_body_2 = {
            "offeringList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            "wantingList": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        res_2 = self.client.post("/api/threads/2/offers", headers=get_api_headers(), data=json.dumps(req_body_2))
        self.assertEqual(res_2.status_code, 201, f"Status code is wrong with message {res_2.data}")

        # Check that trades are in the db and have info
        created_trade_1 = db.session.get(OffersModel, 1)
        created_trade_2 = db.session.get(OffersModel, 2)

        self.assertIsNotNone(created_trade_1)
        self.assertIsNotNone(created_trade_2)

        self.assertEqual(created_trade_1.get_offering(), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(created_trade_1.get_wanting(), [0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(created_trade_1.user_id, 1)
        self.assertEqual(created_trade_1.thread_id, 2)

        self.assertEqual(created_trade_2.get_offering(), [0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(created_trade_2.get_wanting(), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(created_trade_2.user_id, 1)
        self.assertEqual(created_trade_2.thread_id, 2)

        # Check that the trades can be properly accessed through the thread model
        test_thread = db.session.get(ThreadModel, 2)

        self.assertEqual(len(test_thread.offers), 2)
        self.assertEqual(test_thread.offers[0].get_offering(), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(test_thread.offers[1].get_offering(), [0, 0, 0, 0, 1, 0, 0, 0, 0, 0])

    def test_create_for_nonexistent_thread(self):
        """Tests that creating a trade for a nonexistent thread gets the right error response"""

        # Posts a create trade request to a nonexistent thread
        req_body = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res = self.client.post("/api/threads/7/offers", headers=get_api_headers(), data=json.dumps(req_body))
        self.assertEqual(res.status_code, 404, f"Status code is wrong with message {res.data}")

    def test_create_with_wrong_length_lists(self):
        """Tests that creating a trade with wrong length lists gets the right error response"""

        # Posts a create trade request with wrong length lists
        req_body = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res = self.client.post("/api/threads/2/offers", headers=get_api_headers(), data=json.dumps(req_body))
        self.assertEqual(res.status_code, 400, f"Status code is wrong with message {res.data}")

    def test_create_with_negative_items(self):
        """Tests that creating a trade with negative items gets the right error response"""

        # Posts a create trade request with negative items
        req_body = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0, -1],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res = self.client.post("/api/threads/2/offers", headers=get_api_headers(), data=json.dumps(req_body))
        self.assertEqual(res.status_code, 400, f"Status code is wrong with message {res.data}")

    def test_create_with_wrong_item_types(self):
        """Tests that creating a trade with float items gets the right error response"""

        # Posts a create trade request with float items
        req_body = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0.5],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res = self.client.post("/api/threads/2/offers", headers=get_api_headers(), data=json.dumps(req_body))
        self.assertEqual(res.status_code, 400, f"Status code is wrong with message {res.data}")

    def test_thread_owner_creating_trade(self):
        """Tests that the thread owner can't create a trade for their own thread"""

        # Posts a create trade request as the thread owner
        req_body = {
            "offeringList": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "wantingList": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        }
        res = self.client.post("/api/threads/1/offers", headers=get_api_headers(), data=json.dumps(req_body))
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

class TestPerformTrade(BaseApiTest):
    """Tests threads perform trade endpoint - POST api/threads/{thread_id}/offers/{trade_id}"""

    def setUp(self):
        super().setUp()

        # Create a couple of users with auth token directly with the database
        test_user_1 = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_1)

        test_user_2 = UserModel(
            username="test2",
            password_hash="test",
            authentication_token="authtest2",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_2)

        test_user_3 = UserModel(
            username="test3",
            password_hash="test",
            authentication_token="authtest3",
            security_question=3,
            security_question_answer="Purple"
        )

        # Create a couple of new threads directly with the database (user 1)
        test_thread_1 = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        db.session.add(test_thread_1)

        test_thread_2 = ThreadModel(
            title='AAA',
            description='BBB',
            user_id=2
        )
        db.session.add(test_thread_2)

        # Add some items to the users' inventories
        test_user_1.inventory.set_items([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        test_user_2.inventory.set_items([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def tearDown(self):
        super().tearDown()

    def test_valid_perform_trade(self):
        """Tests that trades can be performed from the endpoint"""
        # Create a trade offer (user 2)
        test_offer = OffersModel(
            user_id=2,
            thread_id=1,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer)
        db.session.commit()

        # Posts an accept trade request
        res_1 = self.client.post("/api/threads/1/offers/1", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 204, f"Status code is wrong with message {res_1.data}")

        # Check that the trade has been performed
        test_user_1 = db.session.get(UserModel, 1)
        test_user_2 = db.session.get(UserModel, 2)

        self.assertEqual(test_user_1.inventory.get_items(), [2, 1, 1, 1, 0, 1, 1, 1, 1, 1])
        self.assertEqual(test_user_2.inventory.get_items(), [0, 1, 1, 1, 2, 1, 1, 1, 1, 1])

    def test_trade_not_possible_with_inventories(self):
        """Tests that trades can't be performed if the inventories don't have the items"""

        # Create a trade offer (user 2)
        test_offer = OffersModel(
            user_id=2,
            thread_id=1,
            offering_list=[1, 0, 0, 4, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer)
        db.session.commit()

        # Posts an accept trade request
        res_1 = self.client.post("/api/threads/1/offers/1", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 400, f"Status code is wrong with message {res_1.data}")

        # Check that the trade has not been performed
        test_user_1 = db.session.get(UserModel, 1)
        test_user_2 = db.session.get(UserModel, 2)

        self.assertEqual(test_user_1.inventory.get_items(), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(test_user_2.inventory.get_items(), [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    def test_missing_trade(self):
        """Tests that trades can't be performed if the trade doesn't exist"""

        # Posts an accept trade request
        res_1 = self.client.post("/api/threads/1/offers/1", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 404, f"Status code is wrong with message {res_1.data}")

    def test_missing_thread(self):
        """Tests that trades can't be performed if the thread doesn't exist"""

        # Create a trade offer (user 2)
        test_offer = OffersModel(
            user_id=2,
            thread_id=1,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer)
        db.session.commit()

        # Posts an accept trade request
        res_1 = self.client.post("/api/threads/7/offers/1", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 404, f"Status code is wrong with message {res_1.data}")

    def test_wrong_accepting_user(self):
        """Tests that trades can't be performed if the accepting user is not the thread creator"""

        # Create a trade offer (user 3)
        test_offer = OffersModel(
            user_id=3,
            thread_id=2,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer)
        db.session.commit()

        # Posts an accept trade request (as user 1)
        res_1 = self.client.post("/api/threads/2/offers/1", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 403, f"Status code is wrong with message {res_1.data}")

    def test_trade_for_wrong_thread(self):
        """Tests that trades can't be performed if the trade is for a different thread"""

        # Create some trade offers (user 2)
        test_offer = OffersModel(
            user_id=2,
            thread_id=1,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer)

        test_offer_2 = OffersModel(
            user_id=2,
            thread_id=2,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer_2)
        db.session.commit()

        # Posts an accept trade request
        res_1 = self.client.post("/api/threads/1/offers/2", headers=get_api_headers())
        self.assertEqual(res_1.status_code, 403, f"Status code is wrong with message {res_1.data}")

class TestReadMany(BaseApiTest):
    """Tests threads read many endpoint - GET api/threads/{thread_id}/children"""

    def setUp(self):
        super().setUp()

        # Create a couple of users with auth token directly with the database
        test_user_1 = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_1)

        test_user_2 = UserModel(
            username="test2",
            password_hash="test",
            authentication_token="authtest2",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user_2)

        # Create a couple of new threads directly with the database
        test_thread_1 = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        db.session.add(test_thread_1)

        test_thread_2 = ThreadModel(
            title='AAA',
            description='BBB',
            user_id=2
        )
        db.session.add(test_thread_2)

        # Create a couple of trade offers directly with the database
        test_offer_1 = OffersModel(
            user_id=2,
            thread_id=1,
            offering_list=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        )
        db.session.add(test_offer_1)

        db.session.commit()

    def tearDown(self):
        super().tearDown()

    def test_valid_read_many(self):
        """Tests that trades can be received from the endpoint"""

        # Post a get request for the trade in a thread
        res = self.client.get("/api/threads/1/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Check that the trade is in the response
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 1, f"Data sent back is {res.data}")
        print("AAAAAA", res_json_data[0])

        self.assertEqual(res_json_data[0]["offering"], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], f"Json data sent back is {res_json_data}")
        self.assertEqual(res_json_data[0]["wanting"], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], f"Json data sent back is {res_json_data}")
        self.assertEqual(res_json_data[0]["userId"], 2, f"Json data sent back is {res_json_data[0]['userId']}")
        self.assertEqual(res_json_data[0]["threadId"], 1, f"Json data sent back is {res_json_data[0]['threadId']}")

    def test_get_from_no_trades_thread(self):
        """Tests that getting with no thread children gets an empty list"""

        # Post a get request for the trade in a thread with no trades
        res = self.client.get("/api/threads/2/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Check that the trade is in the response
        res_json_data = json.loads(res.data)
        self.assertEqual(len(res_json_data), 0, f"Data sent back is {res.data}")

    def test_get_from_nonexistent_thread(self):
        """Tests that getting from a nonexistent thread gets the right error response"""

        # Post a get request for the trade in a nonexistent thread
        res = self.client.get("/api/threads/7/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 404, f"Status code is wrong with message {res.data}")

    def test_multiple_children_types(self):
        """Tests that multiple children types can be received from the thread endpoint"""

        # Create a couple of comments directly with the database
        test_comment_1 = CommentModel(
            comment_text="Do you have any with rank above B? I will trade",
            thread_id=1,
            user_id=1
        )
        test_comment_2 = CommentModel(
            comment_text="If u like anything in my inventory I'm down to trade",
            thread_id=1,
            user_id=1
        )
        db.session.add(test_comment_1)
        db.session.add(test_comment_2)
        db.session.commit()

        # Post a get request for all the children in the test thread with two comments
        res = self.client.get("/api/threads/1/children", headers=get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")
        self.assertEqual(len(json.loads(res.data)), 3, f"Data sent back is {res.data}")

        # Check that the children created before are returned with the right information
        res_json_data = json.loads(res.data)

        self.assertEqual(res_json_data[0]["childType"], "offer", f"Json data sent back is {res_json_data[0]['childType']}")
        self.assertEqual(res_json_data[1]["childType"], "comment", f"Json data sent back is {res_json_data[1]['childType']}")
        self.assertEqual(res_json_data[2]["childType"], "comment", f"Json data sent back is {res_json_data[2]['childType']}")

if __name__ == '__main__':
    unittest.main()