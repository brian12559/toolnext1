'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging, time, sys, os
import pytest, unittest
import requests, json, random

# setting the logging module to the console
logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s', level=logging.INFO ,)

class codeBeamerAPItest(unittest.TestCase):
    
    def setUp(self):
        #set variables, load the browser
        logging.info("Function Setup()") 
        logging.info('Current Working Directory: %s' % os.getcwd())


    def tearDown(self):
        #close the browser
        logging.info("Function tearDown()")

    def test_login(self):

        #1st create the test run based on the test set
        res = requests.post(
            "https://codebeamer-devel.hosts.prod.upshift.rdu2.redhat.com:8443/cb/rest/testRun?testSetId=3140",
            auth=('stester1', 'rhtoolnext1'), verify=False)

        print res.status_code
        marker = res.text.find("item") + 5
        testRun = res.text[marker:marker + 5]
        print testRun
       # print res.text

        #for generating random pass fails
        myRan = round(random.random() * 10) + 1
        logging.info(myRan)

        # this gets test case with id = 1001 information, can see this info on screen when you open test case its 3141
        # small one is 5149
        #res = requests.get("https://codebeamer-devel.hosts.prod.upshift.rdu2.redhat.com:8443/cb/api/v2/item/49022",
                           #auth=('bmurray', 'bandg916'), verify=False)
        res = requests.get("https://codebeamer-devel.hosts.prod.upshift.rdu2.redhat.com:8443/cb/api/v2/item/%s" % testRun,
                           auth=('bmurray', 'bandg916'), verify=False)

        print res.status_code
        print res.text
        tests = res.json()

        my_dict = json.loads(res.text)

        # gotta be a better way
        myIDs = []

        for x in my_dict.get('customFields'):
            for key1, value1 in x.iteritems():
                if key1 == 'values':
                    for z in x.get('values'):
                        for q in z:
                            for x_id in q.get('values'):
                                # and finally
                                #print x_id.get("id")
                                myIDs.append(x_id.get("id"))

        # this gets test case with id = 1001 information, can see this info on screen when you open test case
        testdata = {}
        #mylist = []
        xNum = 0
        for myTest in myIDs:
            if xNum == 0:
                testdata = {"%s" % str(myTest): {"success": "true"}}
            xNum = xNum + 1
            y = xNum/myRan
            q=int(xNum/myRan)
            if (y-q==0) and xNum > 1:
                testdata.update({"%s" % str(myTest) : {"success": "false"}})
                #mylist.append({"%s" % str(myTest) : {"success": "false"}})
            else:
                testdata.update({"%s" % str(myTest): {"success": "true"}})
                #mylist.append({"%s" % str(myTest) : {"success": "true"}})
        #testdata.update({"" : mylist})
        time.sleep(2)

        res = requests.post("https://codebeamer-devel.hosts.prod.upshift.rdu2.redhat.com:8443/cb/rest/testRun/%s/result" % testRun,
                        auth=('bmurray', 'bandg916'), verify=False,
                             headers={'content-type': 'application/json'},
                             json=testdata)
        #
        print res.status_code
        print res.text

    def atest_createTR(self):

        res = requests.post(
            "https://codebeamer-devel.hosts.prod.upshift.rdu2.redhat.com:8443/cb/rest/testRun?testSetId=3140",
            auth=('stester1', 'rhtoolnext1'), verify=False)

        print res.status_code
        marker = res.text.find("item") + 5
        print res.text[marker:marker + 5]
        print res.text

if __name__ == "__main__": # allows unittest to start by running this class file
    unittest.main()  
    
    
    