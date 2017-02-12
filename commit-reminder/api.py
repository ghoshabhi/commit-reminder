#!/usr/bin/env python
from flask import Flask, jsonify
from flask_api import FlaskAPI

app = Flask(__name__)

@app.route('/<string:name>')
def sayHello(name):
    resp = "Hello %s !" % name
    return jsonify(resp=resp)

if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
