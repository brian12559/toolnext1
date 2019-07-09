'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging, time, sys, os
import pytest, unittest, random
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
        self.xLimit = 200  #our limit and
        self.tester_id = "stester1"
        self.tester_pw = "!RHtoolnext1"
        self.testSetID = "TOOL3-3537"



    def tearDown(self):
        #close the browser
        logging.info("Function tearDown()")


    def test_login(self):
        #this gets the test ids in the test set 200 at a time and builds the xunit import while doing it
        #when done it sends up the results
        #pass fail mix is random
        myRan = round(random.random() * 10) + 1
        logging.info(myRan)
        tcCount = 0

        #Test execution header info
        mylist = []
        testdata = {
            "info": {
                "summary": "Execution of automated tests for release v1.1; Test Set Imported RHEL tests",
                "description": "This execution is automatically created when importing execution results from an external source",
                "user": self.tester_id,
            }}

        for z in range (1, 200):
            #get results 200 at a time
            res = requests.get("https://projects.devel.engineering.redhat.com/rest/raven/1.0/api/testset/%s/test?limit=%s&page=%s" % (self.testSetID, self.xLimit, z),
                               verify=('/etc/ssl/certs/ca-bundle.crt'),
                               auth=(self.tester_id, self.tester_pw))

            print res.status_code
            print res.text
            if len(res.text)<10:
                break

            x=0;
            while res.text.find("\"key\"", x) > 0:
                keyIndex = res.text.find("\"key\"", x)
                #print keyIndex
                testKey = str(res.text[keyIndex+7:res.text.find("\"id\"", keyIndex)-2])
                print testKey
                tcCount = tcCount + 1
                #randomize the results
                x = res.text.find("\"id\"", keyIndex) + 10
                y = tcCount / myRan
                q = int(tcCount / myRan)
                if (y - q == 0):
                    mylist.append(
                        {'comment': 'Failed execution', 'status': 'FAIL', 'testKey': '%s' % testKey})
                else:
                    mylist.append(
                        {'comment': 'Passed execution', 'status': 'PASS', 'testKey': '%s' % testKey})

            #update the xunit file
            testdata.update({'tests': mylist})
            time.sleep(2)

        #send up the total results
        res = requests.post("https://projects.devel.engineering.redhat.com/rest/raven/1.0/import/execution",
                           auth=(self.tester_id, self.tester_pw),
                           verify=('/etc/ssl/certs/ca-bundle.crt'),
                           headers={'content-type': 'application/json'},
                           json= testdata )

        print res.status_code
        print res.text

if __name__ == "__main__": # allows unittest to start by running this class file
    unittest.main()  
    
    
    