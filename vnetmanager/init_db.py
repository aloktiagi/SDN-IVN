
from vnetmanager import db
from vnetmanager import models

userstatuses = ['Logged Out', 'Logged In', 'Disabled']
users = [('testuser', 'testpass')]

switches = [ 'sw1', 'sw2', 'sw3' ]

links = [ ('sw1', 1, 'sw2'), ('sw2', 1, 'sw1'),
          ('sw1', 2, 'sw3'), ('sw3', 1, 'sw1') ]

def build_links():
    sd = { s.swid: s.id for s in models.NetworkSwitch.query.all() }
    return [ (sd[src], port, sd[dst], -1, 1) for
        (src, port, dst) in links]

def init():
    db.drop_all()
    db.create_all()

    '''
    db.session.add_all(
        map(lambda s: models.UserStatus(s),
            ['Logged Out', 'Logged In', 'Disabled']))
    db.session.commit()
    '''
    db.session.add_all([ models.UserStatus(s) for s in userstatuses ])
    db.session.commit()

    '''
    db.session.add(models.User('testuser', 'testpass'))
    db.session.commit()
    '''
    db.session.add_all([ models.User(*u) for u in users ])
    db.session.commit()

    '''
    db.session.add_all(
        map(lambda s: models.NetworkSwitch(s), ['sw1', 'sw2']))
    db.session.commit()
    '''
    db.session.add_all([ models.NetworkSwitch(s) for s in switches ])
    db.session.commit()

    db.session.add_all([ models.SwitchLink(*l) for l in build_links() ])
    db.session.commit()


