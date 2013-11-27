
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
        models.NetworkTopology.insert().values(
            srcswitch_id=1, srcswitch_port=1, dstswitch_id=2,
            link_capacity=-1, link_cost=1),

        models.NetworkTopology.insert().values(
            srcswitch_id=2, srcswitch_port=1, dstswitch_id=1,
            link_capacity=-1, link_cost=1)
    ]

    for i in ins:
        db.session.execute(i)

    db.session.commit()


