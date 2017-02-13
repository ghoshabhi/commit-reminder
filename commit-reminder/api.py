#!/usr/bin/env python
import requests
from flask import Flask, request, jsonify, session, redirect, \
                 render_template, send_from_directory

from flask_api import FlaskAPI

app = Flask(__name__)
# app.config['GITHUB_CLIENT_ID'] = ''
# app.config['GITHUB_CLIENT_SECRET'] = ''

@app.route('/')
def showLogin():
    return render_template("login.html")

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    code = request.args.get('code')
    print "code: {code}".format(code=code)
    json_header = {'content-type': 'application/json'}

    token_url = "https://{domain}/oauth/token".format(domain='ghoshabhi.auth0.com')

    token_payload = {
        'client_id':     'Loz6vT3OWA0xt6smDzJ8oVprZwcwIwGA',
        'client_secret': '4DhQhrGHsN7QtIi2U-VKVqO6iWj_Z1-2HDYuUtrHXswBPYHDEpDblY6vPM0mmbQk',
        'redirect_uri':  'https://localhost:5000/callback',
        'code':          code,
        'grant_type':    'authorization_code'
    }

    token_info = requests.post(token_url,
                              data=json.dumps(token_payload),
                              headers = json_header) \
                             .json()

    user_url = "https://{domain}/userinfo?access_token={access_token}" \
      .format(domain='ghoshabhi.auth0.com', access_token=token_info['access_token'])

    user_info = requests.get(user_url).json()

    # We're saving all user information into the session
    session['profile'] = user_info

    # Redirect to the User logged in page that you want here
    # In our case it's /dashboard
    return redirect('/hello')

@app.route('/hello')
def sayHello():
    return jsonify(resp="Welcome!")



if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
