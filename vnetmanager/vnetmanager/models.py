from vnetmanager import db

NetworkAccess = db.Table('network_access',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.ForeignKey('user.id')),
    db.Column('virtualnetwork_id', db.Integer,
        db.ForeignKey('virtual_network.id')),
    db.Column('virtualnetworkhost_id',
        db.ForeignKey('virtual_network_host.id')),
    db.Column('active', db.Boolean)
)

class UserStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), unique=True)

    users = db.relationship('User', backref='status', lazy='dynamic')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<UserStatus %r>' % self.description


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50), unique=False)

    status_id = db.Column(db.Integer,
        db.ForeignKey('user_status.id'), default=1)

    authorizednetworks = db.relationship('VirtualNetwork',
        secondary=NetworkAccess, lazy='dynamic')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class PhysicalNetworkHost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(17), unique=True)
    ip = db.Column(db.String(15), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='physicalhost', uselist=False)

    virtualhosts = db.relationship('VirtualNetworkHost', lazy='dynamic')

    switch_id = db.Column(db.Integer, db.ForeignKey('network_switch.id'))
    switch = db.relationship('NetworkSwitch', uselist=False)

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


NetworkTopology = db.Table('network_topology',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('srcswitch_id', db.Integer, db.ForeignKey('network_switch.id')),
    db.Column('srcswitch_port', db.Integer),
    db.Column('dstswitch_id', db.Integer, db.ForeignKey('network_switch.id')),
    db.Column('link_capacity', db.Integer),
    db.Column('link_cost', db.Integer)
)


class NetworkSwitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    swid = db.Column(db.String(50), unique=True)

    hosts = db.relationship('PhysicalNetworkHost', lazy='dynamic')

    '''
    neighbors = db.relationship('NetworkSwitch', secondary=NetworkTopology,
        lazy='dynamic')
    '''

    neighbors = db.relationship('NetworkSwitch',
        secondary=NetworkTopology,
        primaryjoin = id == NetworkTopology.c.srcswitch_id,
        secondaryjoin = id == NetworkTopology.c.dstswitch_id,
        lazy='dynamic')

    def __init__(self, swid):
        self.swid = swid

