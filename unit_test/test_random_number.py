import sys
import os
sys.path.append(os.path.abspath('../'))

from unittest import TestCase
from unittest import mock
from unittest.mock import patch
from icon_unit_test_demo.connection.connection import Connection
from icon_unit_test_demo.triggers.random_number import RandomNumber
import logging
import json
import timeout_decorator


# This will catch timeout errors and return None. This tells the test framework our test passed.
# This is needed because the run function in a trigger is an endless loop.
def timeout_pass(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except timeout_decorator.timeout_decorator.TimeoutError as e:
            print(f"Test timed out as expected: {e}")
            return None

    return func_wrapper

# This mocks komand.Trigger.send
# We need this to fake out the plugin into thinking it's sending output in the trigger's run function
class fakeSender():
    def send(params):
        print(params)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "http://thisisatest":
        return MockResponse({"answer": 10}, 200)

    return MockResponse(None, 404)



# Test class
class TestRandomNumber(TestCase):

    @timeout_pass
    @timeout_decorator.timeout(30)
    @patch("komand.Trigger.send", side_effect=fakeSender.send)
    def test_integration_random_number(self, mockSend):
        """
        TODO: Manually validate results

        Because the send function is essentially an endless loop, there's no way to validate the output from
        that in an elegant way. Really this test is just making sure no exceptions are thrown.

        The bulk of your logic for your trigger should not be in the run loop and should be tested with subsequent
        tests.
        """
        log = logging.getLogger("Test")

        with open("../tests/random_number.json") as f:
            data = json.load(f)
            connection_params = data.get("body").get("connection")
            trigger_params = data.get("body").get("input")

        test_connection = Connection()
        test_connection.logger = log
        test_connection.connect(connection_params)

        test_email_received = RandomNumber()
        test_email_received.connection = test_connection
        test_email_received.logger = log

        test_email_received.run(trigger_params)

        self.fail() # If we made it this far, the run loop failed somehow

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_random_number_some_function_to_test(self, mockPost):
        """
        TODO: Test your trigger logic

        Here and in following tests you should test everything you can in your trigger that's not in the run loop.
        """
        url = "http://thisisatest"

        log = logging.getLogger("Test")
        test_trigger = RandomNumber()
        test_trigger.log = log

        result = test_trigger.get_random_number(url)
        expected = {'answer': 10}

        self.assertEqual(expected, result)
