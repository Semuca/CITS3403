"""Unit tests for loot endpoints"""

from datetime import datetime, timedelta
import unittest
import json

from app.databases import db
from app.models import InventoryModel, INVENTORY_SIZE, UserModel

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
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert inventory has been modified correctly
        self.assertEqual(response_body.get("items"), user.inventory.to_list())

        # Assert level countdown has started
        self.assertGreater(user.level_expiry, datetime.now() + timedelta(days=1,seconds=-5))
        self.assertLess(user.level_expiry, datetime.now() + timedelta(days=1,seconds=5))

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now() + timedelta(hours=12,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now() + timedelta(hours=12,seconds=5))

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
            loot_drop_refresh=datetime.now() - timedelta(seconds=5),
            level_expiry=datetime.now() + timedelta(days=1)
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).to_list()

        # Act
        res = self.client.get("/api/loot", headers=get_api_headers())
        user = db.session.get(UserModel, 1)
        response_body = json.loads(res.data)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now() + timedelta(hours=12,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now() + timedelta(hours=12,seconds=5))

        # Assert inventory has been modified correctly
        current_inventory_list = user.inventory.to_list()
        self.assertEqual(current_inventory_list, [i+j for i,j in zip(old_inventory_list,response_body.get("items"))])
        for i in range(INVENTORY_SIZE): # Make sure all loot items are in range
            self.assertGreaterEqual(current_inventory_list[i], 0)
            self.assertLessEqual(current_inventory_list[i], 4)

    def test_invalid_next_loot(self):
        """Tests that loot will not be collected if user has collected loot under 12 hours ago"""

        # Create new user with auth token directly with the database
        old_loot_drop_refresh = datetime.now() + timedelta(hours=1)
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            loot_drop_refresh=old_loot_drop_refresh,
            level_expiry=datetime.now() + timedelta(days=1)
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).to_list()

        # Act
        res = self.client.get("/api/loot", headers=get_api_headers())
        user = db.session.get(UserModel, 1)

        # Assert inventory hasn't been changed
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

        self.assertEqual(user.inventory.to_list(), old_inventory_list)
        self.assertEqual(user.loot_drop_refresh, old_loot_drop_refresh)

class TestLevelUp(BaseApiTest):
    """Tests level up endpoint - GET api/levelup"""

    def test_valid_level_up(self):
        """Tests that level up will correctly level a player up and speed up the drops an appropriate amount"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now() + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now() + timedelta(hours=11),
        )
        db.session.add(test_user)

        test_user.inventory.query.update({
            'q1': 6,
            'q1_required': 4,
            'q2': 9,
            'q2_required': 2,
        })

        # User is about to level up with 23.5 hours left. Therefore:
        # One loot drop should be triggered. After that, hours left is 23.5 - 11 = 12.5
        # Therefore, another loot drop should be triggered. After that, hours left is 12.5 - 12 = 0.5
        # Therefore, the next loot drop should be 11.5 hours from leveling up

        # Act
        res = self.client.get("/api/levelup", headers=get_api_headers())

        # Assert
        response_body = json.loads(res.data)
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert drops have been received
        drops = response_body.get("drops")
        self.assertEqual(len(drops), 2)

        # Assert level countdown has started
        self.assertGreater(user.level_expiry, datetime.now() + timedelta(days=1,seconds=-5))
        self.assertLess(user.level_expiry, datetime.now() + timedelta(days=1,seconds=5))

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now() + timedelta(hours=11,minutes=30,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now() + timedelta(hours=11,minutes=30,seconds=5))

    def test_invalid_level_up(self):
        """Tests that level up will correctly not level a player up if the requirements are not met"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now() + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now() + timedelta(hours=11),
        )
        db.session.add(test_user)

        test_user.inventory.query.update({
            'q1': 6,
            'q1_required': 9,
            'q2': 9,
            'q2_required': 6,
        })

        # Act
        res = self.client.get("/api/levelup", headers=get_api_headers())

        # Assert
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

if __name__ == '__main__':
    unittest.main()