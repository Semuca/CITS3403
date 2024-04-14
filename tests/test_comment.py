"""Unit test file for the comment model"""

import unittest

from app import create_app
from app.databases import db
from app.models import UserModel, ThreadModel, CommentModel

class TestThreadModel(unittest.TestCase):
    """Tests thread database model"""

    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

        # create new user with auth token directly with the database
        test_user = UserModel(
            username="test",
            password_hash="test",
            authentication_token="authtest"
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
        """Tests adding a thread directly to the database"""

        # Create a new mock Thread object and save to db
        test_comment = CommentModel(
            comment_text="Do you have any with rank above B? I will trade",
            thread_id=1,
            user_id=1
        )
        db.session.add(test_comment)
        db.session.commit()

        # Query for the comment in DB
        created_comment = db.session.get(CommentModel, 1)

        self.assertIsNotNone(created_comment)
        self.assertEqual(created_comment.comment_text, "Do you have any with rank above B? I will trade")
        self.assertEqual(created_comment.user_id, 1)
        self.assertEqual(created_comment.thread_id, 1)

        # Query for the comment from the thread in DB
        created_thread = db.session.get(ThreadModel, 1)

        self.assertIsNotNone(created_thread)
        self.assertEqual(len(created_thread.children), 1)
        self.assertEqual(created_thread.children[0].comment_text, "Do you have any with rank above B? I will trade")
        self.assertEqual(created_thread.children[0].user_id, 1)
        self.assertEqual(created_thread.children[0].thread_id, 1)

if __name__ == '__main__':
    unittest.main()