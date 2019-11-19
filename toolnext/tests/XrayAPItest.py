'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging, time, sys, os
import pytest, unittest
import requests, json
from jira.client import JIRA

# setting the logging module to the console
logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s', level=logging.INFO ,)

class XrayAPItest(unittest.TestCase):
    
    def setUp(self):
        #set variables, load the browser
        logging.info("Function Setup()") 
        logging.info('Current Working Directory: %s' % os.getcwd())
        self.url = "https://projects.devel.engineering.redhat.com"


    def tearDown(self):
        #close the browser
        logging.info("Function tearDown()")

    def actest_login(self):

        #ok, this works...note different url for xray stuff
        #this gets the list of tests in the Test Execution
        res = requests.get("https://projects.devel.engineering.redhat.com/rest/raven/1.0/api/testexec/TOOL1-25926/test",
                           auth=('bmurray@redhat.com', '!BandG0916'))
        print res.status_code
        print res.text

        #returns list of tests in the test execution
        todos = json.loads(res.text)

        time.sleep(2)

        print todos [1]

        for x in todos:
            print x["key"]

    def aaatest_jira(self):
        #YEAH...works
        options = {'server': 'https://projects.devel.engineering.redhat.com', 'verify': '/etc/ssl/certs/ca-bundle.crt'}
        jira = JIRA(options)

    def test_login(self):

#'home/bmurray/jira-develhoststageengrdu2redhatcom.crt',
        res = requests.get("http://jira-dc-servere.hosts.prod.upshift.rdu2.redhat.com/rest/raven/1.0/api/testexec/TOOL1-25926/test",
                verify=('/etc/ssl/certs/ca-bundle.crt'),
                    auth=('bmurray_dev', '!redhat123'))

        print res.status_code
        print res.text

        # my creds dont work..must be wrong auth=('bmurray@redhat.com', '!BandG0916'))


        res = requests.get("http://jira-dc-servere.hosts.prod.upshift.rdu2.redhat.com/rest/raven/1.0/api/testexec/TOOL1-25926/test",
                           verify=('/etc/ssl/certs/ca-bundle.crt'),
                           auth=('bmurray', 'redhat123'))

        print res.status_code
        print res.text

    def atest(self):
        #ok, this works...note different url for xray stuff
        #this gets the list of tests in the Test Execution
        res = requests.get("https://sandbox.xpand-it.com/rest/raven/1.0/api/testexec/TOOL1-26/test",
                           auth=('user31', 'rhtoolnext'))

        print res.status_code
        print res.text

        #this gets the test result for the test case in the test exec
        res = requests.get("https://sandbox.xpand-it.com/rest/raven/1.0/api/testrun?testExecIssueKey=TOOL2-49&testIssueKey=TOOL2-47",
                           auth=('user31', 'rhtoolnext'))
    def btest(self):
        print res.status_code
        print res.text

        #this does the same as above but using the test run ID
        res = requests.get("https://sandbox.xpand-it.com/rest/raven/1.0/api/testrun/4200",
                           auth=('user31', 'rhtoolnext'))

        print res.status_code
        print res.text

        testdata = {
            "status": "FAIL",
        }

        #ok, this works to set a test result to PASS
        #this does the same as above but using the test run ID
        res = requests.put("https://sandbox.xpand-it.com/rest/raven/1.0/api/testrun/4200",
                           auth=('user31', 'rhtoolnext'),
                           headers={'content-type': 'application/json'},
                           json= testdata )

        print res.status_code
        print res.text


if __name__ == "__main__": # allows unittest to start by running this class file
    unittest.main()  
    
    
    