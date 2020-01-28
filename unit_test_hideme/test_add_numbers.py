import sys
import os
sys.path.append(os.path.abspath('../'))

from unittest import TestCase
from unittest import mock
from icon_unit_test_demo.connection.connection import Connection
from icon_unit_test_demo.actions.add_numbers import AddNumbers
import json
import logging

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:5000/add':
        if "num1" in kwargs.get("params") and "num2" in kwargs.get("params"):
            num1 = kwargs.get("params").get("num1")
            num2 = kwargs.get("params").get("num2")
            return MockResponse({"answer": num1 + num2 }, 200)

    return MockResponse(None, 404)

class TestAddNumbers(TestCase):
    def test_integration_add_numbers(self):
        """
        TODO: Implement assertions at the end of this test case

        This is an integration test that will connect to the services your plugin uses. It should be used
        as the basis for tests below that can run independent of a "live" connection.

        This test assumes a normal plugin structure with a /tests directory. In that /tests directory should
        be json samples that contain all the data needed to run this test. For more help on samples run

        icon-plugin --help sample

        """

        log = logging.getLogger("Test")
        test_conn = Connection()
        test_action = AddNumbers()

        test_conn.logger = log
        test_action.logger = log

        with open("../tests/add_numbers.json") as file:
            test_json = json.loads(file.read()).get("body")
            connection_params = test_json.get("connection")
            action_params = test_json.get("input")

        test_conn.connect(connection_params)
        test_action.connection = test_conn
        results = test_action.run(action_params)

        # self.fail("Unimplemented test case")
        self.assertEquals({"answer": 5}, results)

    @mock.patch('requests.post', side_effect=mocked_requests_get)
    def test_add_numbers(self, mockGet):
        """
        TODO: Implement test cases here

        Here you can mock the connection with data returned from the above integration test.
        For information on mocking and unit testing please go here:

        https://docs.google.com/document/d/1PifePDG1-mBcmNYE8dULwGxJimiRBrax5BIDG_0TFQI/edit?usp=sharing

        You can either create a formal Mock for this, or you can create a fake connection class to pass to your
        action for testing.
        """
        log = logging.getLogger("Test")
        test_action = AddNumbers()

        test_action.log = log

        params = {
            "number1": 3,
            "number2": 7
        }

        result = test_action.run(params)

        self.assertEqual({"answer": 10}, result)
