#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/<string:name>')
def sayHello(name):
    resp = "Hello %s !" % name
    return resp

if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
