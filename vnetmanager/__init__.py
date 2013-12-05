#!./flask/bin/python

from flask import Flask
#from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://vnetadmin:password1*@localhost/vNetState'

'''
loginmanager = LoginManager()
loginmanager.init_app(app)
'''

db = SQLAlchemy(app)

from vnetmanager import models, jbapi

'''
@loginmanager.user_loader
def load_user(userid):
    return models.User.query.filter_by(id = int(userid)).first()
'''

