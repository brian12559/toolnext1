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


if __name__ == "__main__":   # allows unittest to start by running this class file
    unittest.main()
