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


from flask_api import FlaskAPI

app = Flask(__name__)

@app.route('/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)

# Using the /callback route to handle authentication.
@app.route('/callback')
def callback_handling():
    print "Hi AJAX!"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter!'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.args.get('code')
    print "code: {code}".format(code=json.dumps(code))

    #json_header = {'content-type': 'application/json'}
    #
    # token_url = "https://{domain}/oauth/token".format(domain='ghoshabhi.auth0.com')
    #
    # token_payload = {
    #     'client_id':     'Loz6vT3OWA0xt6smDzJ8oVprZwcwIwGA',
    #     'client_secret': '4DhQhrGHsN7QtIi2U-VKVqO6iWj_Z1-2HDYuUtrHXswBPYHDEpDblY6vPM0mmbQk',
    #     'redirect_uri':  'https://localhost:5000/callback',
    #     'code':          code,
    #     'grant_type':    'authorization_code'
    # }
    #
    # token_info = requests.post(token_url,
    #                           data=json.dumps(token_payload),
    #                           headers = json_header) \
    #                          .json()
    #
    # user_url = "https://{domain}/userinfo?access_token={access_token}" \
    #   .format(domain='ghoshabhi.auth0.com', access_token=token_info['access_token'])
    #
    # user_info = requests.get(user_url).json()
    #
    # # We're saving all user information into the session
    # session['profile'] = user_info

    # Redirect to the User logged in page that you want here
    # In our case it's /dashboard

@app.route('/hello')
def sayHello():
    return jsonify(resp="Welcome!")



if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
