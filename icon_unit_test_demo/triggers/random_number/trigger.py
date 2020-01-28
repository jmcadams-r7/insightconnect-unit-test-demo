import komand
import time
from .schema import RandomNumberInput, RandomNumberOutput, Input, Output, Component
# Custom imports below
import requests

class RandomNumber(komand.Trigger):

    def __init__(self):
        super(self.__class__, self).__init__(
                name='random_number',
                description=Component.DESCRIPTION,
                input=RandomNumberInput(),
                output=RandomNumberOutput())

    def run(self, params={}):
        # build url
        # url = "http://host.docker.internal:5000/add"
        url = "http://127.0.0.1:5000/random"
        while True:
            dict_ = self.get_random_number(url)

            self.send(dict_)
            time.sleep(params.get("interval", 5))

    def get_random_number(self, url):
        result = requests.get(url)
        json_obj = result.json()
        answer = json_obj.get("answer")
        dict_ = {"answer": answer}
        return dict_
