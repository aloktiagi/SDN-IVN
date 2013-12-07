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
    print request.remote_addr.__class__
    return request.remote_addr + "\n"

@app.route('/api/authenticate', methods = ['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    print username
    user = User.query.filter_by(username=username).first()

    # Could not authenticate
    if user is None:
        flask.abort(403)
    if password != user.password:
        flask.abort(403)

    print user.username
    print user.password


    # Is the user already logged in?
    sessions = user.sessions.filter_by(endtime = None).all()
    # print sessions
    if len(sessions) > 0:
        for s in sessions:
            s.lastactivity = now()
        db.session.commit()
        return jsonify({
            'status': 'successful',
            'message': 'already authenticated' })

    usermac = request.json.get('mac')

    if usermac is None:
        return jsonify({
            'status': 'failed',
            'message': 'please provide mac address'
            })


    userhost = PhysicalNetworkHost.query.filter_by(mac=usermac).first()

    if userhost is None:
        return jsonify({
            'status': 'failed',
            'message': 'could not find mac address'
            })

    us = UserSession(user.id, userhost.id)
    db.session.add(us)
    db.session.commit()

    return jsonify({ 'status':"successful",
        'session_id': us.id })


@app.route('/api/deauthenticate', methods = ['POST'])
def deauthenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    usermac = request.json.get('mac')

    user = User.query.filter_by(username=username).first()

    # Could not authenticate
    if user is None:
        flask.abort(403)
    if password != user.password:
        flask.abort(403)

    if usermac is None:
        return jsonify({
            'status': 'failed',
            'message': 'please provide mac address'
            })

    userhost = PhysicalNetworkHost.query.filter_by(mac=usermac).first()

    if userhost is None:
        return jsonify({
            'status': 'failed',
            'message': 'could not find mac address'
            })

    # Is the user already logged in?
    sessions = user.sessions.all()

    n = now()
    if len(sessions) > 0:
        for s in sessions:
            s.endtime = n
            s.lastactivity = n
            db.session.add(s)
        db.session.commit()
        return jsonify({
            'status': 'successful',
            'message': 'deauthenticated' })

    return jsonify({'status': 'successful', 'message': 'no authenticated sessions existed'})


@app.route('/api/join', methods = ['POST'])
def joinRequest():
    '''
    Request to join a virtual network
    User provides
    '''
    return "network join request"

@app.route('/api/leave', methods = ['POST'])
def leaveRequest():
    return "network leave request"

@app.route('/api/networks', methods = ['GET'])
def networks():
    session_id = int(request.json.get('session_id'))
    usersession = UserSession.query.get(session_id)

    if usersession is None or not usersession.is_active():
        return "you suck"

    nets = { na.id: na.virtualnetwork.vNetID for na in usersession.user.authorizednetworks.all() }

    print nets
    return jsonify(nets)







