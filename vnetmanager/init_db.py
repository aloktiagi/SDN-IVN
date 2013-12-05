
from vnetmanager import db
from vnetmanager import models

switchlink_trigger = "\n".join([
    "CREATE TRIGGER Verify_SwitchLink_%s BEFORE %s ON switch_link",
    "FOR EACH ROW",
    "BEGIN",
    "   DECLARE msg VARCHAR(255);",
    "    IF (NEW.dstswitch_id IS NOT NULL AND NEW.dsthost_id IS NOT NULL) OR",
    "    (NEW.dstswitch_id IS NULL AND NEW.dsthost_id IS NULL) THEN",
    "        SET msg = 'Destination constraint violated.';",
    "        SIGNAL sqlstate '45000' SET message_text = msg;",
    "    END IF;",
    "END;"
])


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

def init():
    db.drop_all()
    db.create_all()

    for s in [("ins", "INSERT"), ("up", "UPDATE")]:
        db.engine.execute(switchlink_trigger % s)

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

