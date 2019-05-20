'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging
import sys
import os
import time
import unittest
import ConfigParser

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pages.base import Page
from pages.logInPage import LoginPage1, LogoutPage
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys

# setting the logging module to the console
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s',
    level=logging.INFO)


class testLabLogin(unittest.TestCase):

    def setUp(self):
        # set variables, load the browser
        logging.info("Function Setup()")
        # the defaults
        self.url = "https://rhtoolnext.melioratestlab.com/testlab/"
        self.user = 'stester1'
        self.password = "rhtoolnext"
        self.browser = "ff"
        self.myLoops = 5
        self.config_file = 'tests/toolnext.ini'

        # read file ini test params file from this folder to get parameters
        if os.path.isfile(self.config_file):
            config = ConfigParser.ConfigParser()
            config.read(self.config_file)
            sectionlist = config.sections()
            section = 'TESTLAB_TEST_PARAMS'
            self.testdatadict = {}
            if section in sectionlist:
                self.testdatadict = dict(config.items(section))
            logging.error(self.testdatadict)
            if 'loops' in self.testdatadict:
                self.myLoops = int(self.testdatadict['loops'])
            if 'user' in self.testdatadict:
                self.user = self.testdatadict['user']
            if 'password' in self.testdatadict:
                self.password = self.testdatadict['password']
            if 'url' in self.testdatadict:
                self.url = self.testdatadict['url']
            if 'browser' in self.testdatadict:
                self.browser = self.testdatadict['browser']

        logging.info("Launching browser -> %s" % self.browser)
        logging.info("Loading url %s" % self.url)
        logging.info("Looping %s times using id=%s and password=%s" % (str(self.myLoops), self.user, self.password))

    def tearDown(self):
        logging.debug("Function tearDown()")

    def test_login(self):
        for z in range(1, self.myLoops+1):
            if self.browser == "ff":
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Chrome()

            # classes used in this file
            self.loader = Page(self.driver)
            self.loginPage = LoginPage1(self.driver)
            self.logoutPage = LogoutPage(self.driver)
            logging.info("Test logging into Testlab")
            logging.info("Loading url %s" % self.url)
            self.loader.open(self.url)
            self.loginPage.login_with_valid_userTL(self.user, self.password)
            time.sleep(1)
            logging.info("Closing browser")
            self.driver.close()
            # for some reason TL thinks something has changed we get
            # a warning dialog
            # this will handle it
            # actions = ActionChains(self.driver)
            # actions.send_keys(Keys.ENTER)
            # actions.perform()


if __name__ == "__main__":   # allows unittest to start
    logging.info("Command Line: %s" % sys.argv)
    unittest.main()
