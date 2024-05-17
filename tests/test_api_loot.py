"""Unit tests for loot and level up endpoints"""

from datetime import datetime, timedelta, timezone
import unittest
import json

from app.databases import db
from app.models import InventoryModel, INVENTORY_SIZE, UserModel

from .helpers import BaseApiTest

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
        res = self.client.get("/api/loot", headers=self.get_api_headers())

        # Assert
        response_body = json.loads(res.data)
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert inventory has been modified correctly
        self.assertEqual(response_body.get("items"), user.inventory.get_items())

        # Assert level countdown has started
        self.assertGreater(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=-5))
        self.assertLess(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=5))

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=12,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=12,seconds=5))

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
            loot_drop_refresh=datetime.now(timezone.utc) - timedelta(seconds=5),
            level_expiry=datetime.now(timezone.utc) + timedelta(days=1)
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).get_items()

        # Act
        res = self.client.get("/api/loot", headers=self.get_api_headers())
        user = db.session.get(UserModel, 1)
        response_body = json.loads(res.data)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=12,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=12,seconds=5))

        # Assert inventory has been modified correctly
        current_inventory_list = user.inventory.get_items()
        self.assertEqual(current_inventory_list, [i+j for i,j in zip(old_inventory_list,response_body.get("items"))])
        for i in range(INVENTORY_SIZE): # Make sure all loot items are in range
            self.assertGreaterEqual(current_inventory_list[i], 0)
            self.assertLessEqual(current_inventory_list[i], 4)

    def test_invalid_next_loot(self):
        """Tests that loot will not be collected if user has collected loot under 12 hours ago"""

        # Create new user with auth token directly with the database
        old_loot_drop_refresh = datetime.now(timezone.utc) + timedelta(hours=1)
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            loot_drop_refresh=old_loot_drop_refresh,
            level_expiry=datetime.now(timezone.utc) + timedelta(days=1),
            level=1
        )
        db.session.add(test_user)

        old_inventory_list = db.session.get(InventoryModel, 1).get_items()

        # Act
        res = self.client.get("/api/loot", headers=self.get_api_headers())
        user = db.session.get(UserModel, 1)

        # Assert inventory hasn't been changed
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

        self.assertEqual(user.inventory.get_items(), old_inventory_list)
        self.assertEqual(user.loot_drop_refresh, old_loot_drop_refresh)

class TestManualLevelUp(BaseApiTest):
    """Tests level up endpoint - GET api/levelup"""

    def test_user_not_playing_yet(self):
        """Tests that a user who has not started playing yet (level 0, before first loot collection) will not be levelled up"""

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
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

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
            level_expiry=datetime.now(timezone.utc) + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now(timezone.utc) + timedelta(hours=11),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([6, 9, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])
        db.session.commit()

        # User is about to level up with 23.5 hours left. Therefore:
        # One loot drop should be triggered. After that, hours left is 23.5 - 11 = 12.5
        # Therefore, another loot drop should be triggered. After that, hours left is 12.5 - 12 = 0.5
        # Therefore, the next loot drop should be 11.5 hours from leveling up

        # Act
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        response_body = json.loads(res.data)
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert drops have been received
        drops = response_body.get("drops")
        self.assertEqual(len(drops), 2)

        # Assert level countdown has started
        self.assertGreater(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=-5))
        self.assertLess(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=5))

        # Assert loot drop countdown has started
        self.assertGreater(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=11,minutes=30,seconds=-5))
        self.assertLess(user.loot_drop_refresh, datetime.now(timezone.utc) + timedelta(hours=11,minutes=30,seconds=5))

    def test_valid_level_up_no_loot(self):
        """Tests that levelling up with a higher loot drop cooldown will not trigger any loot drops"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now(timezone.utc) + timedelta(hours=42),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([6, 9, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])
        db.session.commit()

        # Act
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert inventory is still the same
        self.assertEqual(user.inventory.get_items(), [2, 7, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_valid_level_up_one_drop(self):
        """Tests that levelling up with a lower loot drop cooldown will trigger one loot drop"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now(timezone.utc) + timedelta(hours=20),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([6, 9, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])
        db.session.commit()

        # Act
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        response_body = json.loads(res.data)
        user = db.session.get(UserModel, 1)

        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert inventory has only been through one loot drop
        max_loot = 4 * INVENTORY_SIZE + 9 # 9 is leftover after subtraction
        min_loot = 9
        loot_count = sum(user.inventory.get_items())
        self.assertLessEqual(loot_count, max_loot)
        self.assertGreaterEqual(loot_count, min_loot)

    def test_invalid_level_up_no_loot(self):
        """Tests that level up will correctly not level a player up if the requirements are not met"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) + timedelta(hours=23, minutes=30),
            loot_drop_refresh=datetime.now(timezone.utc) + timedelta(hours=11),
        )
        db.session.add(test_user)

        test_user.inventory.set_items([6, 9, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([9, 6, 0, 0, 0, 0, 0, 0, 0, 0])
        db.session.commit()

        # Act
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

class TestAutoLevelling(BaseApiTest):
    """Tests auto levelling, which may level up or down a player if the time is up based on if requirements are met"""

    def test_user_not_playing_yet(self):
        """Tests that a user who has not started playing yet (level 0, before first loot collection) will not be levelled up or down"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
        )
        db.session.add(test_user)

        # Act
        res = self.client.get("/api/levelup", headers=self.get_api_headers())

        # Assert
        self.assertEqual(res.status_code, 403, f"Status code is wrong with message {res.data}")

    def test_user_auto_levelup_once(self):
        """Tests that a user will level up once if the time is up, when relevant pages are visited"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) - timedelta(seconds=5),
            loot_drop_refresh=datetime.now(timezone.utc) - timedelta(seconds=5),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([6, 9, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])

        # Act
        res = self.client.get("/api/users", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert
        user = db.session.get(UserModel, 1)
        self.assertEqual(user.level, 2)
        self.assertLess(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=15))
        self.assertGreater(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=-15))
        self.assertLess(user.loot_drop_refresh, datetime.now(timezone.utc))
        self.assertEqual(user.inventory.get_items(), [2, 7, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_user_auto_levelup_multiple(self):
        """Tests that a user will level up multiple times is more than a day overtime but with inventory to last"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) - timedelta(days=1, seconds=5), # triggers 2 level expiries
            loot_drop_refresh=datetime.now(timezone.utc) - timedelta(days=2),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([30, 30, 30, 30, 30, 30, 30, 30, 30, 30])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])

        # Act
        res = self.client.get("/api/users", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert
        user = db.session.get(UserModel, 1)
        self.assertEqual(user.level, 3)
        self.assertLess(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=15))
        self.assertGreater(user.level_expiry, datetime.now(timezone.utc) + timedelta(days=1,seconds=-15))
        self.assertLess(user.loot_drop_refresh, datetime.now(timezone.utc))

    def test_user_auto_leveldown(self):
        """Tests that a user will level down if the time is up and requirements are not met"""

        # Create new user with auth token directly with the database
        test_user = UserModel(
            id=1,
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple",
            level_expiry=datetime.now(timezone.utc) - timedelta(seconds=5),
            loot_drop_refresh=datetime.now(timezone.utc) - timedelta(seconds=5),
            level=1
        )
        db.session.add(test_user)

        test_user.inventory.set_items([3, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        test_user.inventory.set_items_required([4, 2, 0, 0, 0, 0, 0, 0, 0, 0])

        # Act
        res = self.client.get("/api/users", headers=self.get_api_headers())
        self.assertEqual(res.status_code, 200, f"Status code is wrong with message {res.data}")

        # Assert
        user = db.session.get(UserModel, 1)
        self.assertEqual(user.level, 0)
        self.assertIsNone(user.level_expiry)
        self.assertIsNone(user.loot_drop_refresh)
        self.assertEqual(user.inventory.get_items(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(user.inventory.get_items_required(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

if __name__ == '__main__':
    unittest.main()
