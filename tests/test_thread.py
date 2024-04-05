"""Unit test file for thread.py"""

import unittest

from main import create_app, db
from models.thread import ThreadModel

class TestThread(unittest.TestCase):
    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app()
        self.appContext = self.app.app_context()
        self.appContext.push()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.appContext.pop()

    def testAddThread(self):
        # Create a new mock Thread object and save to db
        testThread = ThreadModel(
            title='Exchange rare cards',
            description = "I'm looking for a green mage to improve defence. Anyone willing to trade one for an explode bot?",
            userId=234090
        )

        db.session.add(testThread)
        db.session.commit()

        # Query for threads in DB
        createdThread = db.session.get(ThreadModel, 1)

        # Assert that the created Thread object exists and has info
        self.assertIsNotNone(createdThread)
        self.assertEqual(createdThread.title, 'Exchange rare cards')
        self.assertEqual(createdThread.userId, 234090)

if __name__ == '__main__':
    unittest.main()