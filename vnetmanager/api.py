import models

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/authenticate', methods = ['POST'])
def authenticate(username, password):
    user = models.User.query.filter_by(
        username = username, password = password)

    if user is None:
        pass

    else:
        pass

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

