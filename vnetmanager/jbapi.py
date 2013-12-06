import flask
from vnetmanager import db, app
from vnetmanager.models import *
import cgi
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired


@app.route('/')
def index():
    '''
    #users = models.User.query.all()
    users = User.query.all()
    users = "<ul><li>%s</li></ul>" % "</li><li>".join(
        [cgi.escape(str(u)) for u in users])
    users = "<h3>Users</h3>" + users

    return "<html><body>%s</body></html>" % users
    '''
    print "Alok"
    return 'hello world!'


@app.route('/api/authenticate', methods = ['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    print username
    user = User.query.filter_by(username=username).first()
    print user.username
    print user.password

    # Could not authenticate
    if user is None:
        flask.abort(403)
    if password != user.password:
        flask.abort(403)

    # Is the user already logged in?
    #sessions = user.sessions.filter_by(endtime = None).all()
    #print sessions
    #if len(sessions) > 0:
    #    for s in sessions:
    #        s.lastactivity = now()
    #    db.session.commit()
    #    return 'Already logged in!'
    return jsonify({ 'username':"alok" })


'''
@app.route('/api/deauthenticate', methods = ['POST'])
def deauthenticate():
    return "deauthenticate"

@app.route('/api/join', methods = ['POST'])
def joinRequest():
    return "network join request"

@app.route('/api/leave', methods = ['POST'])
def leaveRequest():
    return "network leave request"

@app.route('/api/networks', methods = ['GET']):
def networks():
    return "laskfjsaldjfkas"
'''
