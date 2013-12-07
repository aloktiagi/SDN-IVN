from vnetmanager import db
from datetime import datetime

def now():
    return datetime.utcnow()

'''
NetworkAccess = db.Table('network_access',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.ForeignKey('user.id')),
    db.Column('virtualnetwork_id', db.Integer,
        db.ForeignKey('virtual_network.id')),
    db.Column('virtualnetworkhost_id',
        db.ForeignKey('virtual_network_host.id')),
    db.Column('active', db.Boolean)
)
'''

class NetworkAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    virtualnetwork_id = db.Column(db.Integer,
        db.ForeignKey('virtual_network.id'))

    virtualnetworkhost_id = db.Column(db.Integer,
        db.ForeignKey('virtual_network_host.id'))

    virtualnetwork = db.relationship('VirtualNetwork', uselist=False)

    active = db.Column(db.Boolean)

    def __init__(self, user_id, vnetwork_id, vhost_id=None, active=False):
        self.user_id = user_id
        self.virtualnetwork_id = vnetwork_id
        self.virtualnetworkhost_id = vhost_id
        self.active = active


class UserStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True)

    users = db.relationship('User', backref='status', lazy='dynamic')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<UserStatus %r>' % self.description


class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    physicalhost_id = db.Column(db.Integer,
        db.ForeignKey('physical_network_host.id'))
    starttime = db.Column(db.DateTime, default=datetime.utcnow)
    endtime = db.Column(db.DateTime)
    lastactivity = db.Column(db.DateTime)

    user = db.relationship('User', uselist=False)
    physicalhost = db.relationship('PhysicalNetworkHost', uselist=False)

    def __init__(self, userid, hostid, start=now(), end=None, lastact=None):
        self.user_id = userid
        self.physicalhost_id = hostid
        self.starttime = start
        self.endtime = end
        self.lastactivity = lastact

    def __repr__(self):
        return '<UserSession %r>' % self.id

    def is_active(self):
        return self.endtime is None




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=False)

    status_id = db.Column(db.Integer,
        db.ForeignKey('user_status.id'), default=1)

    authorizednetworks = db.relationship('NetworkAccess', lazy='dynamic')

    sessions = db.relationship('UserSession', lazy='dynamic')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)


    # is_authenticated(), is_active(), is_anonymous(), get_id() are required
    # for use with flask-login
    def is_authenticated(self):
        return len(self.sessions.filter_by(endtime = None).all()) > 0

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)



class PhysicalNetworkHost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17), unique=True)
    ip = db.Column(db.String(15), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='physicalhost', uselist=False)

    virtualhosts = db.relationship('VirtualNetworkHost', lazy='dynamic')

    '''
    switch_id = db.Column(db.Integer, db.ForeignKey('network_switch.id'))
    switch_port = db.Column(db.Integer)
    switch = db.relationship('NetworkSwitch', uselist=False)
    '''

    # def __init__(self, mac, ip, switch, port, user=None):
    def __init__(self, mac, ip, user=None):
        self.mac = mac
        self.ip = ip
        self.user = user

    def __repr__(self):
        return '<PhysicalNetworkHost %r>' % self.mac

class VirtualNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vNetID = db.Column(db.String(32), unique=True)
    vlan = db.Column(db.Integer, unique=True)
    cidr = db.Column(db.String(18))

    hosts = db.relationship('VirtualNetworkHost',
        backref='virtualnetwork', lazy='dynamic')

    def __init__(self, vNetID, vlan, cidr):
        self.vNetID = vNetID
        self.vlan = vlan

        # TODO: cidr validation (make sure networks don't overlap, etc)
        self.cidr = cidr

    def __repr__(self):
        return ('<VirtualNetwork vNetID: %r, VLAN: %d, CIDR: %r' %
            (self.vNetID, self.vlan, self.cidr))


class VirtualNetworkHost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17), unique=True)
    ip = db.Column(db.String(15), unique=True)

    physicalhost_id = db.Column(db.Integer,
        db.ForeignKey('physical_network_host.id'))
    physicalhost = db.relationship('PhysicalNetworkHost', uselist=False)

    virtualnetwork_id = db.Column(db.Integer,
        db.ForeignKey('virtual_network.id'))

    def __init__(self, mac, ip, physicalhost_id, physicalhost):
        self.mac = mac
        self.ip = ip
        self.physicalhost = physicalhost

    def __repr__(self):
        return '<PhysicalNetworkHost %r>' % self.mac


'''
SwitchLink = db.Table('network_topology',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('srcswitch_id', db.Integer, db.ForeignKey('network_switch.id')),
    db.Column('srcswitch_port', db.Integer),
    db.Column('dstswitch_id', db.Integer, db.ForeignKey('network_switch.id')),
    db.Column('link_capacity', db.Integer),
    db.Column('link_cost', db.Integer)
)
'''

class SwitchLink(db.Model):

    __table_args__ = (db.UniqueConstraint('srcswitch_id', 'srcswitch_port'),)

    id = db.Column(db.Integer, primary_key=True)
    srcswitch_id = db.Column(db.Integer, db.ForeignKey('network_switch.id'))
    srcswitch_port = db.Column(db.Integer)
    dstswitch_id = db.Column(db.Integer, db.ForeignKey('network_switch.id'))
    dsthost_id = db.Column(db.Integer,
        db.ForeignKey('physical_network_host.id'))
    capacity = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    dsthost = db.relationship('PhysicalNetworkHost', uselist=False)

    dstswitch = db.relationship('NetworkSwitch', foreign_keys=[dstswitch_id], uselist=False)

    def __init__(self, src_id, src_port, dst_id,
        dsttype='switch', capacity=-1, cost=1):

        if dsttype not in ('switch', 'host'):
            raise Exception('Invalid dsttype')

        self.srcswitch_id = src_id
        self.srcswitch_port = src_port
        self.dstswitch_id = dst_id if dsttype == 'switch' else None
        self.dsthost_id = dst_id if dsttype == 'host' else None
        self.capacity = capacity
        self.cost = cost

    def __repr__(self):
        format = "SwitchLink %r:\n" \
               + "\tsrcswitch_id: %r\n\tsrcswitch_port: %r\n" \
               + "\tdstswitch_id: %r\n\tdsthost_id: %r\n\n"
        return format % (self.id, self.srcswitch_id, self.srcswitch_port,
            self.dstswitch_id, self.dsthost_id)


class NetworkSwitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swid = db.Column(db.String(50), unique=True)

    links = db.relationship('SwitchLink',
        primaryjoin = id == SwitchLink.srcswitch_id,
        lazy='dynamic')

    def __init__(self, swid):
        self.swid = swid

    def __repr__(self):
        return '<NetworkSwitch %r>' % self.swid

    # Returns a list of tuples (<neighbor>, <port>, <cost>) where:
    #   - <neighbor> is a NetworkSwitch instance representing the neighbor
    #   - <port> is the number of current switch's port that is connected to
    #       <neighbor>
    #   - <cost> is the cost of the link for Dijkstra's algorithm

    def getneighborlinks(self, returnquery=False):
        query = self.links.filter_by(dsthost_id = None)
        return query if returnquery else query.all()

    def getneighbors(self):
        return [ (l.dstswitch, l.srcswitch_port, l.cost)
            for l in self.getneighborlinks() ]

    def gethostlinks(self, returnquery=False):
        query = self.links.filter_by(dstswitch_id = None)
        return query if returnquery else query.all()

    def gethosts(self):
        return [ (l.dsthost, l.srcswitch_port, l.cost)
            for l in self.gethostlinks() ]

