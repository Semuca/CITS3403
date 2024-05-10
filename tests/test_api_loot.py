"""Unit tests for loot endpoints"""

from datetime import datetime, timedelta
import unittest
import json

from app.databases import db
from app.models import InventoryModel, UserModel

from .helpers import BaseApiTest, get_api_headers

class TestGetLoot(BaseApiTest):
    """Tests loot drop endpoint - GET api/loot"""

    def test_valid_first_loot(self):
        """Tests that loot can be collected if user has never collected loot"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user)

        # Act
        res = self.client.get("/api/loot", headers=get_api_headers())

        # Assert
        response_body = json.loads(res.data)
        inventory = db.session.get(InventoryModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert inventory has been modified correctly
        self.assertIsNotNone(inventory)
        self.assertEqual(response_body.get("items"), inventory.to_list())

    def test_valid_next_loot(self):
        """Tests that loot can be collected if user has collected loot over 12 hours ago"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            last_drop_collected=(datetime.now() - timedelta(hours=12))
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).to_list()

        # Act
        res = self.client.get("/api/loot", headers=get_api_headers())
        inventory = db.session.get(InventoryModel, 1)
        response_body = json.loads(res.data)

        # Assert inventory has been modified correctly
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")
        self.assertEqual(inventory.to_list(), [i+j for i,j in zip(old_inventory_list,response_body.get("items"))])

    def test_invalid_next_loot(self):
        """Tests that loot will not be collected if user has collected loot under 12 hours ago"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            last_drop_collected=(datetime.now() - timedelta(hours=11))
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).to_list()

        # Act
        res = self.client.get("/api/loot", headers=get_api_headers())
        inventory = db.session.get(InventoryModel, 1)

        # Assert inventory hasn't been changed
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")
        self.assertEqual(inventory.to_list(), old_inventory_list)

if __name__ == '__main__':
    unittest.main()
