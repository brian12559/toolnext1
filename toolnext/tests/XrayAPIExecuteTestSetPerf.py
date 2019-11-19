'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging, time, sys, os
import pytest, unittest, random
import requests, json
import ConfigParser
from jira.client import JIRA

# setting the logging module to the console
logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s', level=logging.INFO ,)

class XrayAPItest(unittest.TestCase):
    
    def setUp(self):
        #set variables, load the browser
        logging.info("Function Setup()") 
        logging.info('Current Working Directory: %s' % os.getcwd())
        self.url = "https://projects.devel.engineering.redhat.com"
        self.xLimit = 200  #was 200 our limit and current Jira API limit
        self.tester_id = "bmurray"
        self.tester_pw = "redhat123"
        self.testSetID = "TOOL1-25930"
        self.maxLoops = 2
        # read file ini test params file from this folder to get parameters
        if (os.path.isfile('toolnext.ini')):
            config = ConfigParser.ConfigParser()
            config.read('toolnext.ini')
            sectionlist = config.sections()
            section = 'XRAY_TEST_PARAMS'
            self.testdatadict = {}
            if section in sectionlist:
                self.testdatadict = dict(config.items(section))
            if ('resloops' in self.testdatadict):
                self.maxLoops = int(self.testdatadict['resloops'])
            if ('user' in self.testdatadict):
                self.tester_id = self.testdatadict['user']
            if ('password' in self.testdatadict):
                self.tester_pw = self.testdatadict['password']

    def tearDown(self):
        #close the browser
        logging.info("Function tearDown()")


    def test_login(self):
        for xLoops in range (1, self.maxLoops):
            startloading = time.time()
            myRan = round(random.random() * 10) + 1
            logging.info(myRan)
            #this gets the test ids in the test set 200 at a time and builds the xunit import while doing it
            #when done it sends up the results
            #pass fail mix is random

            tcCount = 0

            #Test execution header info
            mylist = []
            testdata = {
                "info": {
                    "summary": "Execution of Test Set->Imported RHEL tests, release v1.%s, tester=%s; " % (xLoops, self.tester_id),
                    "description": "This execution is automatically created when importing execution results from an external source",
                    "user": self.tester_id,
                }}

            for z in range (1, 200):  #was 200

                #get results 200 at a time
                res = requests.get("http://jira-dc-servere.hosts.prod.upshift.rdu2.redhat.com/rest/raven/1.0/api/testset/%s/test?limit=%s&page=%s" % (self.testSetID, self.xLimit, z),
                                   verify=('/etc/ssl/certs/ca-bundle.crt'),
                                   auth=(self.tester_id, self.tester_pw))

                #print res.status_code
                #print res.text
                if len(res.text)<10:
                    break

                x=0;
                while res.text.find("\"key\"", x) > 0:
                    keyIndex = res.text.find("\"key\"", x)
                    #print keyIndex
                    testKey = str(res.text[keyIndex+7:res.text.find("\"id\"", keyIndex)-2])
                    #print testKey
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
            res = requests.post("http://jira-dc-servere.hosts.prod.upshift.rdu2.redhat.com/rest/raven/1.0/import/execution",
                               auth=(self.tester_id, self.tester_pw),
                               verify=('/etc/ssl/certs/ca-bundle.crt'),
                               headers={'content-type': 'application/json'},
                               json= testdata )
            logging.info("Results Upload took " + str((time.time() - startloading)) + " seconds")
            print res.status_code
            print res.text

if __name__ == "__main__": # allows unittest to start by running this class file
    unittest.main()  
    
    
    