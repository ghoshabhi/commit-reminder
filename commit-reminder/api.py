#!/usr/bin/env python
import requests
from flask import Flask, request, jsonify, redirect, \
                 render_template, send_from_directory, url_for
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
request_url = 'https://api.github.com'

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
        #return jsonify(code=request.args.get('code'))
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        req = requests.post(token_url, params=payload, headers=headers)
        resp = req.json()

        if 'access_token' in resp:
            #return jsonify(access_token=resp['access_token'])
            login_session['access_token'] = resp['access_token']
            return redirect(url_for('index'))
        else:
            return jsonify(error="Github didn't return access_token")
    else:
        return jsonify(error="404_no_code")

@app.route('/index')
def index():
    # authenticated?
    if not 'access_token' in login_session:
        return 'Never trust strangers', 404
    # get username from github api
    url = 'https://api.github.com/user?access_token={}'
    r = requests.get(url.format(login_session['access_token']))
    try:
        resp = r.json()
        gh_profile = resp['html_url']
        username = resp['login']
        avatar_url = resp['avatar_url']
        bio = resp['bio']
        name = resp['name']
        return render_template("profile.html",
                                name=name,
                                avatar_url=avatar_url,
                                username=username,
                                bio=bio,
                                gh_profile=gh_profile)
    except AttributeError:
        app.logger.debug('error getting username from github, whoops')
        return "I don't know who you are; I should, but regretfully I don't", 500
    # return 'Hello {}!'.format(login), 200

@app.route('/hello')
def sayHello():
    return jsonify(resp="Welcome!")

@app.route('/user/<string:username>')
def getRepos(username):
    if not 'access_token' in login_session:
        invalid_access_token="Access token has expired or not in session"
        app.logger.error(invalid_access_token)
        return jsonify(invalid_access_token=invalid_access_token)
    if not username:
        return jsonify(username_not_give="Github username needed to fetch \
                                         repos")
    url = request_url + '/users/{username}/repos'.format(username=username)
    headers = {'Accept': 'application/json'}
    req = requests.get(url, headers=headers)
    resp = req.json()
    try:
        app.logger.debug("Try to get repository names from response")
        repo_info = []
        for each_repo in resp:
            repo_dict = {}
            repo_dict['repo_name'] = each_repo['full_name']
            repo_dict['repo_link'] = each_repo['html_url']
            repo_dict['description'] = each_repo['description']
            repo_dict['owner_fullname'] = each_repo['owner']['login']
            repo_dict['html_url'] = each_repo['html_url']
            repo_info.append(repo_dict)
        app.logger.debug("Successfully fetched repository info from response")
        #return jsonify(repo_info)
        #print json.dumps(repo_info)
        return render_template("repo.html", repo_info=repo_info)
    except (TypeError, AttributeError, KeyError), e:
        app.logger.error(e)
        return jsonify(no_user_found="no user found")


if __name__ == "__main__":
    app.secret_key = "fart_fart"
    app.debug = True
    app.run()
