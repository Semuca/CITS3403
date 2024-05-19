"""System tests for home page"""

import os
import unittest

from app.databases import db
from app.models import UserModel

from .helpers import BaseSeleniumTest, getPath

@unittest.skipIf(os.environ['SKIP_PAGE_TESTS'] == "true", "SKIP_PAGE_TESTS is flagged")
class TestBasePage(BaseSeleniumTest):
    """Tests the base page wrapper"""

    def test_unauthenticated_base(self):
        """Tests unauthenticated navigation using the base page wrapper"""

        # Navigating to the home page should work successfully
        link = self.driver.find_element('id', 'home-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/')

        # Navigating to the sign up page should work successfully
        link = self.driver.find_element('id', 'sign-up-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/register')

        # Navigating to the log in page should work successfully
        link = self.driver.find_element('id', 'log-in-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/login')

        # Navigating to the forum page should redirect to the login page if unauthenticated
        link = self.driver.find_element('id', 'forum-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/login')

        # Navigating to the game page should redirect to the login page if unauthenticated
        link = self.driver.find_element('id', 'game-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/login')

        # Navigating to the profile page should redirect to the login page if unauthenticated
        link = self.driver.find_element('id', 'profile-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/login')

    def test_authenticated_base(self):
        """Tests authenticated navigation using the base page wrapper"""

        # Assemble
        db.session.add(UserModel(
            username="PurpleGuy",
            description="I'm the man behind the slaughter",
            password_hash="Password123",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="idk"
        ))
        db.session.commit()

        self.driver.add_cookie({'name': 'token', 'value': 'authtest'})

        # Navigating to the home page should work successfully
        link = self.driver.find_element('id', 'home-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/')

        # Navigating to the sign up page should work successfully
        link = self.driver.find_element('id', 'sign-up-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/register')

        # Navigating to the log in page should work successfully
        link = self.driver.find_element('id', 'log-in-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/login')

        # Navigating to the forum page should work successfully
        link = self.driver.find_element('id', 'forum-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/forum')

        # Navigating to the game page should work successfully
        link = self.driver.find_element('id', 'game-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/game')

        # Navigating to the profile page should work successfully
        link = self.driver.find_element('id', 'profile-nav-link')
        link.click()

        self.assertEqual(getPath(self.driver.current_url), '/profile')


if __name__ == '__main__':
    unittest.main()
