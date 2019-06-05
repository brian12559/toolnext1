'''
Created on Aug 31, 2018

@author: bmurray
'''

import logging, time, sys, os
import pytest, unittest
import requests

# setting the logging module to the console
logging.basicConfig(format='%(asctime)s [%(levelname)s] (%(threadName)-2s) %(message)s', level=logging.INFO, )


class ptAPItest(unittest.TestCase):

    def setUp(self):
        # set variables, load the browser
        logging.info("Function Setup()")
        logging.info('Current Working Directory: %s' % os.getcwd())

    def tearDown(self):
        # close the browser
        logging.info("Function tearDown()")

    def test_login(self):
        # curl -H "Content-Type: application/json" \
        #     -u user@pt.com:dd2d9ddee2e9cd4861b1f0353375de1b4444d49  \
        #    https://api.practitest.com/api/v2/projects.json

        import httplib
        import requests
        from requests.auth import AuthBase
        import json

        data_json = json.dumps(
            {'data': [{'type': 'instances', 'attributes': {'instance-id': 15821792,
                                                           'exit-code': 0, 'automated-execution-output': 'my output'}},
                      {'type': 'instances', 'attributes': {'instance-id': 15821793,
                                                           'exit-code': 0, 'automated-execution-output': 'my output'}},
                      {'type': 'instances', 'attributes': {'instance-id': 15960866,
                                                           'exit-code': 0, 'automated-execution-output': 'my output'}},
                      {'type': 'instances', 'attributes': {'instance-id': 15960867,
                                                           'exit-code': 1, 'automated-execution-output': 'my output'}}
                      ]
             })

        r = requests.post("https://api.practitest.com/api/v2/projects/12457/runs.json",
                          data=data_json,
                          auth=('bmurray@redhat.com', '71589219464455f81e3a6c684ca86d363e8819f3'),
                          headers={'Content-type': 'application/json'})

        print r.status_code
        print r.text

        # time.sleep(1)


if __name__ == "__main__":  # allows unittest to start by running this class file
    unittest.main()


