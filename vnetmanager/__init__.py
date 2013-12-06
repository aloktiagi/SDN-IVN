#!./flask/bin/python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://vnetadmin:password1*@localhost/vNetState'

db = SQLAlchemy(app)

from vnetmanager import init_db, models, jbapi

init_db.initialize()




