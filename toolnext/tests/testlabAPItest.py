'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging
import time
import sys
import os
import pytest
import unittest
import requests

# setting the logging module to the console
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s',
    level=logging.INFO)


class testlabAPItest(unittest.TestCase):

    PROJECT_KEY = 'TLABTMPL'
    PROJECT_NAME = 'ToolNext'
    USER = 'smanager1'
    API_KEY = '550e8400-e29b-41d4-a716-44665544'

    def setUp(self):
        """
        Set variables, load the browser
        """
        logging.info("Function Setup()")
        logging.info('Current Working Directory: %s' % os.getcwd())

    def tearDown(self):
        """
        Close the browser
        """
        logging.info("Function tearDown()")

    def test_login(self):
        # This works
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/defect/%s' % self.PROJECT_NAME,
                           auth=('user', self.API_KEY))
        logging.debug("%s - %s" % (res.status_code, res.text))
        #assert res.ok   # this fails with 404

        # Works to get all test cases in project=TLABTMPL
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/testcase/%s' % self.PROJECT_KEY,
                           auth=('user', self.API_KEY))
        logging.debug("%s - %s" % (res.status_code, res.text))
        assert res.ok

        # Works to get the single test case data
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/testcase/%s/227091' % self.PROJECT_KEY,
                           auth=('user', self.API_KEY))
        logging.debug("%s - %s" % (res.status_code, res.text))
        assert res.ok

    def test_upload_results_data(self):
        count_of_results = 3500

        def _generate_results(count):
            results = []
            for i in range(count):
                test_name = "myAutomatedTest%s" % i
                result = i % 3
                comment = "Test %s with result %s" % (test_name, result)
                results.append({
                    "mappingId": test_name,
                    "result": result,
                    "started": 1487250019387 + i,
                    "run": 1487250019987 + i + 1,
                    "comment": comment,
                })
            return results

        data = {
          "projectKey": self.PROJECT_KEY,
          "testRunTitle": "Automated run %s" % time.time(),
          "comment": "Some comment text bound to the test run",
          "status": 3,
          "user": self.USER,

          "milestoneIdentifier": "A2",
          "milestoneTitle": "myAutomatedMilestoneTitle 2",
          "testTargetTitle": "myAutomatedTestTargetTitle",
          "testEnvironmentTitle": "myAutomatedTest",
          "tags": "myAutomatedTag1 myAutomatedTag2",

          "addIssues": False,
          "mergeAsSingleIssue": False,
          "reopenExistingIssues": False,
          "assignIssuesToUser": self.USER,

          "testCaseMappingField": "Automated",
          "importTestCases": True,
          "importTestCasesRootCategory": "import",

          #"robotCatenateParentKeywords": true
          #"xml": "<jUnit/xUnit XML content or Robot Framework output XML>",
          #"xmlFormat": "junit | robot",
          "results": _generate_results(count_of_results),
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json;charset=UTF-8',
        }
        logging.debug("Sending data: %s" % data)
        before = time.time()
        res = requests.put('https://rhtoolnext.melioratestlab.com/api/testresult',
                           auth=('user', self.API_KEY), json=data, headers=headers)
        after = time.time()
        logging.info("Upload of %s results via data took %.2f secods succesfull? %s" \
            % (count_of_results, after-before, res.ok))
        assert res.ok, "Response text: %s" % res.text


if __name__ == "__main__":   # allows unittest to start by running this class file
    unittest.main()
