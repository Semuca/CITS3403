"""Unit test file for thread.py"""

import unittest

from main import createApp, db
from databases.thread import Thread

class TestThread(unittest.TestCase):
    def setUp(self):
        self.app = createApp()
        self.app_context = self.app.app_context()
        self.app_context.push()        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_thread(self):
        # Create a new Thread object
        test_thread = Thread(
            title='Exchange rare cards',
            description = "I'm looking for a green mage to improve defence. Anyone willing to trade one for an explode bot?",
            createdAt='040404',
            userId=234090
        )

        # Save to db
        db.session.add(test_thread)
        db.session.commit()

        # Query for threads in DB
        created_thread = db.session.get(Thread, 1)

        # Assert that the created Thread object exists and has info
        self.assertIsNotNone(created_thread)
        self.assertEqual(created_thread.title, 'Exchange rare cards')

if __name__ == '__main__':
    unittest.main()