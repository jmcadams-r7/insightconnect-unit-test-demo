# GENERATED BY KOMAND SDK - DO NOT EDIT
import komand
import json


class Component:
    DESCRIPTION = "Add Numbers"


class Input:
    NUMBER1 = "number1"
    NUMBER2 = "number2"
    

class Output:
    ANSWER = "answer"
    

class AddNumbersInput(komand.Input):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "number1": {
      "type": "integer",
      "title": "Number1",
      "description": "A Number",
      "order": 1
    },
    "number2": {
      "type": "integer",
      "title": "Number2",
      "description": "A Number",
      "order": 2
    }
  },
  "required": [
    "number1",
    "number2"
  ]
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)


class AddNumbersOutput(komand.Output):
    schema = json.loads("""
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "answer": {
      "type": "integer",
      "title": "Answer",
      "description": "Answer",
      "order": 1
    }
  },
  "required": [
    "answer"
  ]
}
    """)

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)
