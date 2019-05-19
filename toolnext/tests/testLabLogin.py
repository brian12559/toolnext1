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
from optparse import OptionParser

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
        self.url = "https://rhtoolnext.melioratestlab.com/testlab/"
        # the defaults
        self.user = 'stester1'
        self.password = "rhtoolnext"
        self.browser = "ff"
        self.myLoops = 5

        # read file ini test params file from this folder to get parameters
        if (os.path.isfile('toolnext.ini')):
            config = ConfigParser.ConfigParser()
            config.read('toolnext.ini')
            sectionlist = config.sections()
            section = 'TESTLAB_TEST_PARAMS'
            self.testdatadict = {}
            if section in sectionlist:
                self.testdatadict = dict(config.items(section))
            if ('loops' in self.testdatadict):
                self.myLoops = int(self.testdatadict['loops'])
            if ('user' in self.testdatadict):
                self.user = self.testdatadict['user']
            if ('password' in self.testdatadict):
                self.password = self.testdatadict['password']
            if ('url' in self.testdatadict):
                self.url = self.testdatadict['url']

        logging.info("Launching browser -> %s" % self.browser)
        logging.info("loading url %s" % self.url)
        logging.info("looping %s times using id=%s and password=%s" % (str(self.myLoops), self.user, self.password))

    def tearDown(self):
        # close the browser
        logging.debug("Function tearDown()")
        # self.driver.close()

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
            logging.info("Test logging into Xray")
            logging.info("loading url %s" % self.url)
            self.loader.open(self.url)   # or this
            self.loginPage.login_with_valid_userTL(self.user, self.password)
            time.sleep(1)
            logging.info("Closing browser")
            # self.driver.quit()
            self.driver.close()
            # for some reason TL thinks something has changed we get
            # a warning dialog
            # this will handle it
            # actions = ActionChains(self.driver)
            # actions.send_keys(Keys.ENTER)
            # actions.perform()


if __name__ == "__main__":   # allows unittest to start
    argv = sys.argv[1:]

    # command line parser
    parser = OptionParser(usage='%prog [options] ', version='0.1',)
    parser.add_option("-n", "--loops", dest="myLoops", default=10,
                      help='Defines how many cycles')

    # read the command line parameters now
    (options, args) = parser.parse_args(argv)
    myLoops = options.loops
    logging.info("Command Line: %s" % sys.argv)
    logging.info(options.loops)

    unittest.main()
