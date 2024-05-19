"""System tests for home page"""

import os
from selenium.webdriver.support.ui import WebDriverWait
import unittest

from app.databases import db
from app.models import ThreadModel, UserModel

from .helpers import BaseSeleniumTest, getPath, LOCALHOST

@unittest.skipIf(os.environ.get('SKIP_PAGE_TESTS') == "true", "SKIP_PAGE_TESTS is flagged")
class TestForumPage(BaseSeleniumTest):
    """Tests the forum page"""

    def setUp(self):
        super().setUp()

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            description="I'm the man behind the slaughter",
            password_hash="8d5647a456007ba44c5095cf21197f161853166ee32acfa19eb8a7ce3b41d3c5",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="idk"
        ))

        db.session.add(ThreadModel(
            title='Exchange rare cards',
            description = "looking for a green mage to improve defence.",
            user_id=1
        ))
        db.session.commit()

        # Add authentication cookie
        self.driver.add_cookie({'name': 'token', 'value': 'authtest'})

        # Navigate to position and wait to load
        self.driver.get(LOCALHOST + '/forum')

    def test_forum_navigation(self):
        """Tests valid forum navigation"""

        WebDriverWait(self.driver, 3).until(
            lambda d: d.find_element('id', 'thread-1')
        )

        # Navigating to the home page should work successfully
        first_thread = self.driver.find_element('id', 'thread-1')
        first_thread.click()

        self.assertEqual(getPath(self.driver.current_url), '/thread/1')

if __name__ == '__main__':
    unittest.main()
