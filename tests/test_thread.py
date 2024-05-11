"""Unit test file for the thread model"""

import unittest

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

if __name__ == '__main__':
    unittest.main()
