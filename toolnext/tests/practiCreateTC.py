'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging
import sys,os
import time
import datetime
import unittest
import ConfigParser
from optparse import OptionParser

sys.path.insert(0, os.path.dirname(os.path.dirname( __file__ )))

from pages.base import Page
from pages.logInPage import LoginPage1, LogoutPage
from selenium import webdriver

# setting the logging module to the console
logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s', level=logging.INFO ,)


class practiCreateTC(unittest.TestCase):

    def setUp(self):
        #set variables, load the browser
        logging.info("Function Setup()")
        self.url = 'https://prod.practitest.com/'
        self.url = "https://prod.practitest.com/"
        #the defaults
        self.user = 'bmurray@redhat.com'
        self.password = "!RHtoolnext1"
        self.browser="ff"
        self.myLoops = 5

        # read file ini test params file from this folder to get parameters
        if (os.path.isfile('toolnext.ini')):
            config = ConfigParser.ConfigParser()
            config.read('toolnext.ini')
            sectionlist = config.sections()
            section = 'PRACTITEST_TEST_PARAMS'
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
        logging.info("loading url %s" %self.url)
        logging.info("looping %s times using id=%s and password=%s" % (str(self.myLoops), self.user, self.password))
         
    def tearDown(self):
        #close the browser
        logging.debug("Function tearDown()")
       # self.driver.close()
        

    def test_login(self):
        homedir = os.path.expanduser('~')
        for z in range(1,self.myLoops+1):
            if self.browser == "ff":
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.Chrome()


            #set title of test
            myTitle = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            myTitle = "test automagically created at %s" % myTitle
            # classes used in this file
            self.loader = Page(self.driver)
            self.loginPage = LoginPage1(self.driver)
            self.logoutPage = LogoutPage(self.driver)
            logging.info("Test logging into PractiTest")
            logging.info("loading url %s" % self.url)
            self.loader.open(self.url) #or this
            try:
                startloading = time.time()
                self.loginPage.login_with_valid_userPT(self.user, self.password)
                #time.sleep(1)
                self.loginPage.createTCPT(myTitle)
                #wait 10 seconds for success message
                while not ('success' in self.driver.page_source):
                    time.sleep(1)
                if ('success' in self.driver.page_source):
                    logging.info("%s created successfully" % myTitle)
                    ltime = str((time.time() - startloading))
                    logging.info("time to load PractiTest and Create a Test Case -> %s" % ltime)
                    with open("%s/LoginCreateTCtime.csv" % homedir, "a") as myfile:
                        myfile.write(time.ctime() + "," + ltime + "\n")
                else:
                    logging.info("test failed to create")

            except:
                logging.info("failed to login or create test case")

            logging.info("Closing browser")
            self.driver.quit()

if __name__ == "__main__": # allows unittest to start by running this class file
    #global loglevel 
    argv = sys.argv[1:]
    
    # command line parser
    parser = OptionParser(usage='%prog [options] ', version='0.1',)
    parser.add_option("-n", "--loops", dest="myLoops", default=10, help='Defines how many cycles')
    
    # read the command line parameters now
    (options, args) = parser.parse_args(argv)
    myLoops=options.loops
    logging.info("Command Line: %s" % sys.argv)
    logging.info(options.loops)
    
    unittest.main() 
    