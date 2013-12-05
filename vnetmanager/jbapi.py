import flask
from vnetmanager import db, app
from vnetmanager.models import *
import cgi

@app.route('/')
def index():
    '''
    #users = models.User.query.all()
    users = User.query.all()
    users = "<ul><li>%s</li></ul>" % "</li><li>".join(
        [cgi.escape(str(u)) for u in users])
    users = "<h3>Users</h3>" + users

    return "<html><body>%s</body></html>" % users
    '''
    return 'hello world!'


@app.route('/api/authenticate', methods = ['POST'])
def authenticate(username, password):
    user = User.query.filter_by(username=username, password=password).first()

    # Could not authenticate
    if user is None:
        flask.abort(403)

    # Is the user already logged in?
    sessions = user.sessions.filter_by(endtime = None).all()
    if len(sessions) > 0:
        for s in sessions:
            s.lastactivity = now()
        db.session.commit()
        return 'Already logged in!'


'''
@app.route('/api/deauthenticate', methods = ['POST'])
def deauthenticate():
    return "deauthenticate"

@app.route('/api/join', methods = ['POST'])
def joinRequest():
    return "network join request"

@app.route('/api/leave', methods = ['POST'])
def leaveRequest():
    return "network leave request"

@app.route('/api/networks', methods = ['GET']):
def networks():
    return "laskfjsaldjfkas"
'''
