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
        company = 'ToolNext'
        apiKey = '550e8400-e29b-41d4-a716-44665544'
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/defect/ToolNext',
                           auth=('user', apiKey))
        logging.debug("%s - %s" % (res.status_code, res.text))
        #assert res.ok   # this fails with 404

        # Works to get all test cases in project=TLABTMPL
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/testcase/TLABTMPL',
                           auth=('user', apiKey))
        logging.debug("%s - %s" % (res.status_code, res.text))
        assert res.ok

        # Works to get the single test case data
        res = requests.get('https://rhtoolnext.melioratestlab.com/api/testcase/TLABTMPL/227091',
                           auth=('user', apiKey))
        logging.debug("%s - %s" % (res.status_code, res.text))
        assert res.ok

    def test_aaa(self):
        apiKey = '550e8400-e29b-41d4-a716-44665544'
        data = {
          "projectKey": "TLABTMPL",
          "testRunTitle": "Automated run 3",
          "comment": "Some comment text bound to the test run",
          "status": 3,
          "user": "smanager1",
          "milestoneIdentifier": "A2",
          "milestoneTitle": "myAutomatedMilestoneTitle 2",
          "testTargetTitle": "myAutomatedTestTargetTitle",
          "testEnvironmentTitle": "myAutomatedTest",
          "tags": "myAutomatedTag1 myAutomatedTag2",
          "testCaseMappingField": "Automated",
          "addIssues": False,
          "mergeAsSingleIssue": False,
          "reopenExistingIssues": False,
          "assignIssuesToUser": "stester1",
          "importTestCases": True,
          "importTestCasesRootCategory": "import",
          #"robotCatenateParentKeywords": true
          #"xml": "<jUnit/xUnit XML content or Robot Framework output XML>",
          #"xmlFormat": "junit | robot",
          "results": [
            {
              "mappingId": "myAutomatedTest1",
              "result": 1,
              "started": 1487250019387,
              "run": 1487250019987,
              "runBy": "selenium-agent",
              "comment": "Timeout occurred",
              "steps": [
                {
                  "result": 1,
                  "description": "Navigate to the site",
                  "expected": "Front page of the site opens up",
                  "comment": "the loading time of the page was nicely snappy",
                  "custom1": "A value for first custom field",
                },
                {
                  "result": 2,
                  "description": "...",
                  "expected": "...",
                  "comment": "...",
                  "custom1": "...",
                }
              ]
            },
            {
              "mappingId": "myAutomatedTest2",
              "result": 3,
              "started": 1558005552000,
              "run": 1558005752000,
              "runBy": "selenium-agent",
              "comment": "...",
              "steps": [
                {
                  "result": 4,
                  "description": "...",
                  "expected": "...",
                  "comment": "...",
                  "custom1": "...",
                },
                {
                  "result": 5,
                  "description": "...",
                  "expected": "...",
                  "comment": "...",
                  "custom1": "...",
                }
              ]
            }
          ],
        }
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json;charset=UTF-8',
        }
        res = requests.put('https://rhtoolnext.melioratestlab.com/api/testresult',
                           auth=('user', apiKey), json=data, headers=headers)
        print(res.ok)
        print(res.status_code)
        print(res.text)


if __name__ == "__main__":   # allows unittest to start by running this class file
    unittest.main()
