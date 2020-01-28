import flask
from flask import request, jsonify
from random import seed, randint

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Joey's number magic!</h1><p>This is a demo for python unit testing.</p>"

@app.route('/add', methods=["POST", "GET"])
def add():
    if not 'num1' in request.args or not 'num2' in request.args:
        return "Error: Need two numbers to add"

    ret_payload = {
        "answer": int(request.args['num1']) + int(request.args['num2'])
    }

    return ret_payload

@app.route('/random', methods=["POST", "GET"])
def random():
    ret_payload = {
        "answer": randint(0, 10)
    }

    return ret_payload

app.run()
