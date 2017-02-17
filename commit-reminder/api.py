#!/usr/bin/env python
import requests
from flask import Flask, request, jsonify, redirect, \
                 render_template, send_from_directory
from flask import session as login_session
from flask import make_response
import json
import requests
import random
import string
from credentials import client_id, client_secret

from flask_api import FlaskAPI

app = Flask(__name__)

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

@app.route('/handleLogin', methods=["GET"])
def handleLogin():
    if login_session['state'] == request.args.get('state'):
        print login_session['state']
        fetch_url = authorization_base_url + \
                    '?client_id=' + client_id + \
                    '&state=' + login_session['state'] + \
                    '&scope=user%20repo%20public_repo' + \
                    '&allow_signup=true'
        print fetch_url
        return redirect(fetch_url)
    else:
        return jsonify(invalid_state_token="invalid_state_token")


@app.route('/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)

# Using the /callback route to handle authentication.
@app.route('/callback', methods=['GET', 'POST'])
def callback_handling():
    print "Hi AJAX!"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if 'code' in request.args:
        return jsonify(code=request.args.get('code'))
    else:
        return jsonify(error="404_no_code")


@app.route('/hello')
def sayHello():
    return jsonify(resp="Welcome!")



if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
