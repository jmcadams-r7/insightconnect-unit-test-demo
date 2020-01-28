import komand
import requests
from .schema import AddNumbersInput, AddNumbersOutput, Input, Output, Component

# Custom imports below


class AddNumbers(komand.Action):

    def __init__(self):
        super(self.__class__, self).__init__(
                name='add_numbers',
                description=Component.DESCRIPTION,
                input=AddNumbersInput(),
                output=AddNumbersOutput())

    def run(self, params={}):
        num1 = params.get(Input.NUMBER1)
        num2 = params.get(Input.NUMBER2)

        params = {
            "num1": num1,
            "num2": num2
        }

        # build url
        # url = "http://host.docker.internal:5000/add"
        url = "http://127.0.0.1:5000/add"

        result = requests.post(url, params=params)
        retval = result.json()
        answer = retval.get("answer")


        return {"answer": answer}
