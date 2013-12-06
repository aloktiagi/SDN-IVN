
from vnetmanager import db, models, db_triggers

userstatuses = ['inactive', 'active', 'authenticated']
users = [('testuser', 'testpass')]

switches = [ 'sw1', 'sw2', 'sw3' ]

links = [ ('sw1', 1, 'sw2'), ('sw2', 1, 'sw1'),
          ('sw1', 2, 'sw3'), ('sw3', 1, 'sw1') ]

# (srcswitch, port, host)
hostlinks = [ ('sw2', 2, 1), ('sw2', 3, 2), ('sw3', 2, 3), ('sw3', 3, 4) ]

def build_links():
    sd = { s.swid: s.id for s in models.NetworkSwitch.query.all() }
    return [ (sd[src], port, sd[dst]) for
        (src, port, dst) in links] + [ (sd[src], port, host, 'host')
        for (src, port, host) in hostlinks ]

physhosts = [
    ('00:00:00:00:00:01', '10.0.0.1'),
    ('00:00:00:00:00:02', '10.0.0.2'),
    ('00:00:00:00:00:03', '10.0.0.3'),
    ('00:00:00:00:00:04', '10.0.0.4')
]

vnets = [
    ('10', 10, '10.10.10.0/24'),
    ('20', 20, '10.10.20.0/24'),
    ('30', 30, '10.10.30.0/24')
]

access = [ (1, 1), (1, 2), (1, 3) ]

def init():
    db.drop_all()
    initialize()

    db.session.add_all([ models.UserStatus(s) for s in userstatuses ])
    db.session.commit()

    db.session.add_all([ models.User(*u) for u in users ])
    db.session.commit()

    db.session.add_all([ models.NetworkSwitch(s) for s in switches ])
    db.session.commit()

    db.session.add_all([ models.PhysicalNetworkHost(*h) for h in physhosts ])
    db.session.commit()

    db.session.add_all([ models.SwitchLink(*l) for l in build_links() ])
    db.session.commit()

    db.session.add_all([ models.VirtualNetwork(*v) for v in vnets])
    db.session.commit()

    db.session.add_all([ models.NetworkAccess(*a) for a in access ])
    db.session.commit()




def initialize():
    db.create_all()

    existing_triggers = [ t[0] for t in
        db.session.execute('SHOW TRIGGERS;').fetchall() ]

    triggers = db_triggers.gettriggers()
    for t in triggers.keys():
        if t not in existing_triggers:
            db.session.execute(triggers[t])
