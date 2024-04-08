"""Unit test file for thread.py"""

import unittest

from app import create_app
from app.databases import db
from app.models import ThreadModel

class TestThread(unittest.TestCase):
    """Tests thread database operations"""

    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_thread(self):
        """Tests adding a thread to the database"""

        # Create a new mock Thread object and save to db
        test_thread = ThreadModel(
            title='Exchange rare cards',
            description = """I'm looking for a green mage to improve defence.
                            Anyone willing to trade one for an explode bot?""",
            userId=234090
        )

        db.session.add(test_thread)
        db.session.commit()

        # Query for threads in DB
        created_thread = db.session.get(ThreadModel, 1)

        # Assert that the created Thread object exists and has info
        self.assertIsNotNone(created_thread)
        self.assertEqual(created_thread.title, 'Exchange rare cards')
        self.assertEqual(created_thread.userId, 234090)

if __name__ == '__main__':
    unittest.main()
