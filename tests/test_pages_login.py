"""System tests for home page"""

import os
from selenium.webdriver.support.ui import WebDriverWait
import unittest

from app.databases import db
from app.models import UserModel

from .helpers import BaseSeleniumTest, getPath, LOCALHOST

@unittest.skipIf(os.environ.get('SKIP_PAGE_TESTS') == "true", "SKIP_PAGE_TESTS is flagged")
class TestLoginPage(BaseSeleniumTest):
    """Tests the login page"""

    def setUp(self):
        super().setUp()
        db.session.add(UserModel(
            username="PurpleGuy",
            description="I'm the man behind the slaughter",
            password_hash="8d5647a456007ba44c5095cf21197f161853166ee32acfa19eb8a7ce3b41d3c5",
            authentication_token="authtest",
            security_question=3,
            security_question_answer="idk"
        ))
        db.session.commit()

        self.driver.get(LOCALHOST + '/login')

    def test_valid_login(self):
        """Tests valid login"""

        # Navigating to the home page should work successfully
        username = self.driver.find_element('id', 'username')
        username.send_keys('PurpleGuy')

        password = self.driver.find_element('id', 'password')
        password.send_keys('Password123')

        login_button = self.driver.find_element('id', 'pressLogin')
        login_button.click()

        WebDriverWait(self.driver, 3).until(lambda x: getPath(x.current_url) == '/forum')

        self.assertEqual(getPath(self.driver.current_url), '/forum')

    def test_invalid_login(self):
        """Tests valid login"""

        # Navigating to the home page should work successfully
        username = self.driver.find_element('id', 'username')
        username.send_keys('PurpleGuy')

        password = self.driver.find_element('id', 'password')
        password.send_keys('idk')

        login_button = self.driver.find_element('id', 'pressLogin')
        login_button.click()

        WebDriverWait(self.driver, 3)

        self.assertEqual(getPath(self.driver.current_url), '/login')

if __name__ == '__main__':
    unittest.main()
