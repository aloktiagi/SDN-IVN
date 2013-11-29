
from vnetmanager import db
from vnetmanager import models

def init():
    db.drop_all()
    db.create_all()

    db.session.add_all(
        map(lambda s: models.UserStatus(s),
            ['Logged Out', 'Logged In', 'Disabled']))
    db.session.commit()

    db.session.add(models.User('testuser', 'testpass'))
    db.session.commit()

    db.session.add_all(
        map(lambda s: models.NetworkSwitch(s), ['sw1', 'sw2']))
    db.session.commit()

    ins = [
        models.NetworkTopology(1, 1, 2, -1, 1),
        models.NetworkTopology(2, 1, 1, -1, 1)
    ]

    db.session.add_all(ins)
    db.session.commit()


