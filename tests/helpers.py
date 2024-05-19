"""Helper functions for tests"""

import multiprocessing
import unittest
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from app import create_app
from app.databases import db

multiprocessing.set_start_method("fork")

LOCALHOST = "http://localhost:5000"

class BaseApiTest(unittest.TestCase):
    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # create all tables in the db
        db.create_all()

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

def get_api_headers():
    """Gets basic headers for testing api requests"""
    return {
        'Authorization': 'Bearer ' + "authtest",
        'Accept': '*/*',
        'Content-Type': 'application/json'
    }

class BaseSeleniumTest(unittest.TestCase):
    def setUp(self):
        # create app so db can be linked to it
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # create all tables in the db
        db.create_all()

        self.server_process = multiprocessing.Process(target=lambda : self.app.run(debug=True, use_reloader=False), daemon=True)
        self.server_process.start()

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("-headless")

        self.driver = webdriver.Chrome()
        self.driver.get(LOCALHOST)

        WebDriverWait(self.driver, 1)

    def tearDown(self):
        # stop db session and clear out all data
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()

        self.driver.quit()

def getPath(url):
    return urlparse(url).path

