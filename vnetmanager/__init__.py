#!./flask/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from vnetmanager import db_triggers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://vnetadmin:password1*@localhost/vNetState'

db = SQLAlchemy(app)

existing_triggers = [ t[0] for t in
    db.session.execute('SHOW TRIGGERS;').fetchall() ]

triggers = db_triggers.gettriggers()
for t in triggers.keys():
    if t not in existing_triggers:
        db.session.execute(triggers[t])


from vnetmanager import models, jbapi




