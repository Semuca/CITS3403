"""Unit test file for the trade model"""

import unittest

from app import create_app
from app.databases import db
from app.models import UserModel, ThreadModel, OffersModel, CommentModel

class TestOffersModel(unittest.TestCase):
    """Tests trade database model"""

    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="Purple"
        )
        db.session.add(test_user)

        # create new thread with user directly with the database
        test_thread = ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        )
        db.session.add(test_thread)

        db.session.commit()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add(self):
        """Tests adding a trade directly to the database"""

        # Create a new mock Trade object and save to db
        test_trade = OffersModel(
            user_id=1,
            thread_id=1,
            offering_list=[1, 2, 3, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 4, 5, 6, 0, 0, 0, 0]
        )
        db.session.add(test_trade)
        db.session.commit()

        # Query for the trade in DB
        created_trade = db.session.get(OffersModel, 1)

        self.assertIsNotNone(created_trade)
        self.assertEqual(created_trade.get_offering(), [1, 2, 3, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(created_trade.get_wanting(), [0, 0, 0, 4, 5, 6, 0, 0, 0, 0])
        self.assertEqual(created_trade.user_id, 1)
        self.assertEqual(created_trade.thread_id, 1)

        # Query for the trade from the thread in DB
        created_thread = db.session.get(ThreadModel, 1)

        self.assertIsNotNone(created_thread)
        self.assertEqual(len(created_thread.children), 1)
        self.assertEqual(created_thread.children[0].get_offering(), [1, 2, 3, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(created_thread.children[0].get_wanting(), [0, 0, 0, 4, 5, 6, 0, 0, 0, 0])
        self.assertEqual(created_thread.children[0].user_id, 1)
        self.assertEqual(created_thread.children[0].thread_id, 1)
        self.assertEqual(created_thread.children[0].thread_child_type, "offer")

    def test_thread_multiple_children_types(self):
        """Tests adding multiple children types (both comment and offer) to a thread"""

        # Create a new mock Comment object and save to db
        test_comment = CommentModel(
            comment_text="Do you have any with rank above B? I will trade",
            thread_id=1,
            user_id=1
        )
        db.session.add(test_comment)

        # Create a new mock Trade object and save to db
        test_trade = OffersModel(
            user_id=1,
            thread_id=1,
            offering_list=[1, 2, 3, 0, 0, 0, 0, 0, 0, 0],
            wanting_list=[0, 0, 0, 4, 5, 6, 0, 0, 0, 0]
        )
        db.session.add(test_trade)
        db.session.commit()

        # Query for the thread in DB
        created_thread = db.session.get(ThreadModel, 1)

        self.assertIsNotNone(created_thread)
        self.assertEqual(len(created_thread.children), 2)

        self.assertEqual(created_thread.children[0].thread_child_type, "comment")
        self.assertEqual(created_thread.children[0].comment_text, "Do you have any with rank above B? I will trade")
        self.assertEqual(created_thread.children[0].user_id, 1)
        self.assertEqual(created_thread.children[0].thread_id, 1)

        self.assertEqual(created_thread.children[1].thread_child_type, "offer")
        self.assertEqual(created_thread.children[1].get_offering(), [1, 2, 3, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(created_thread.children[1].get_wanting(), [0, 0, 0, 4, 5, 6, 0, 0, 0, 0])
        self.assertEqual(created_thread.children[1].user_id, 1)
        self.assertEqual(created_thread.children[1].thread_id, 1)

if __name__ == '__main__':
    unittest.main()