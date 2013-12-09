import flask
from vnetmanager import db, app, utils, flow_pusher, graph
from vnetmanager.models import *
from vnetmanager.flow_pusher import *
from vnetmanager.graph import *
from vnetmanager.switchflow import *
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
    user = User.query.filter_by(username=username).first()

    # Could not authenticate
    if user is None:
        flask.abort(403)
    if password != user.password:
        flask.abort(403)

    # Is the user already logged in?
    sessions = user.sessions.filter_by(endtime = None).all()
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
    vnetid = request.json.get('vnetwork_id')
    session_id = request.json.get('session_id')
    usermac = request.json.get('mac')
    userhost = PhysicalNetworkHost.query.filter_by(mac=usermac).first()

    usersession = UserSession.query.get(int(session_id))

    if usersession is None or not usersession.is_active():
        return "asfdjiasfljsadfa"

    vnet = VirtualNetwork.query.filter_by(vNetID = vnetid).first()

    if vnet is None:
        return "lkafslkjasfdas"

    ip = str(vnet.generateIP())
    mac = utils.generateMAC()

    vNetHost = VirtualNetworkHost(mac, ip, userhost.id, vnet.id, session_id)
    db.session.add(vNetHost)
    db.session.commit()
    '''
    ADD FLOWS
    '''

    myswitchlink = SwitchLink.query.filter_by(dsthost=userhost).first()
    myswitch = NetworkSwitch.query.filter_by(id = myswitchlink.srcswitch_id).first()
    #flow = FlowPusher()
    #flow.addflow(myswitch.swid, mac, vnet.vlan, myswitchlink.srcswitch_port)
    #print myswitch

    vNetHosts = VirtualNetworkHost.query.all()
    if len(vNetHosts) > 0:
        for vhost in vNetHosts:
            switchlink = SwitchLink.query.filter_by(dsthost_id=vhost.physicalhost_id).first()
            switch = NetworkSwitch.query.filter_by(id = switchlink.srcswitch_id).first()
            if switch.swid != myswitch.swid:
                print 'Switches myswitch {} switch {}'.format(myswitch.swid,switch.swid)
                traverse = graph.dijkstra(myswitch.swid,switch.swid)
                print 'Traverse {}'.format(traverse)
                addMultiSwitchFlows(traverse,mac,vhost.mac)
            

    #switchlink = SwitchLink.query.filter_by(dsthost=userhost).first()
    #switch = NetworkSwitch.query.filter_by(id = switchlink.srcswitch_id).first()
    #flow = FlowPusher()
    #flow.addflow(switch.swid, mac, vnet.vlan, switchlink.srcswitch_port)
    #print switch
    

    return jsonify({'status': 'successful',
        'ip': ip,
        'mac': mac })

@app.route('/api/leave', methods = ['POST'])
def leaveRequest():
    vnetid = request.json.get('vnetwork_id')
    session_id = request.json.get('session_id')

    usersession = UserSession.query.get(int(session_id))

    if usersession is None or not usersession.is_active():
        return "asfdjiasfljsadfa"

    vnet = VirtualNetwork.query.filter_by(vNetID=vnetid).first()
    vhosts = usersession.virtualhosts.filter_by(virtualnetwork_id = vnet.id).all()

    print vhosts

    for vh in vhosts:
        db.session.delete(vh)
        db.session.commit()

    return "gtfo"

@app.route('/api/networks', methods = ['GET'])
def networks():
    session_id = int(request.json.get('session_id'))
    usersession = UserSession.query.get(session_id)

    if usersession is None or not usersession.is_active():
        return "you suck"

    nets = { na.id: na.virtualnetwork.vNetID for na in usersession.user.authorizednetworks.all() }

    print nets
    return jsonify(nets)







