# app stuff...
from functools import wraps # auth
from flask import (Flask, 
        render_template, 
        request, 
        Response,  
        json)

# db stuff... 
from database import db_session, init_db
from model.Pages import Pages
from model.Password import Password


# new app + make db connection
app = Flask(__name__)
init_db()

# ============
# AUTH METHODS
# ============

def check_auth(username, password):
    """Check valid username/password combos.
    """
    for _pass in db_session.query(Password.password).filter(Password.id == 1):
        if _pass.password == password and username == 'admin':
            return True
    return False 

def authenticate():
    """Sends a 401 response that enables basic auth.
    """
    return Response('Could not verify you.\n', 401, 
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Decorator that requires auth.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            if auth is not None:
                app.logger.critical('Failed auth attempt for: %s, %s' 
                        % (auth.username, auth.password))
            return authenticate()
        return f(*args, **kwargs)
    return decorated
            

# =======================
# Routing and controllers
# =======================

@app.route('/')
@requires_auth
def hello():
    return render_template('home.html')

@app.route('/save', methods=['POST'])
def save():
    if request.method != 'POST':
        return 405 #not allowed
    _json = request.get_json
    app.logger.info(_json)
    #p = Pages(contents="It worked!")
    #db_session.add(p)
    #db_session.commit()
    return 200

@app.route('/get', methods=['GET'])
def get_page():
    if request.method != 'POST':
        return 405 #not allowed
    return 200

# ==================
# ERROR HANDLER PAGE
# ==================

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return render_template('500.html'), 500

# ==================
# ERROR HANDLER PAGE
# ==================
@app.teardown_appcontext
def shutdown_session(exception=None):
    app.logger.debug('teardown')
    db_session.remove()
