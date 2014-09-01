# NOTE: This is just a demo app, so I've included all of the controller 
#       and view codes in this file.
#
# app stuff...
from functools import wraps # auth
from flask import (Flask, 
        render_template, 
        request, 
        Response,  
        json, 
        jsonify)

# db stuff... 
from database import db_session, init_db
from model.Pages import Pages
from model.Password import Password
from sqlalchemy import func, update


# new app + make db connection
app = Flask(__name__)
init_db()

# ==================
# BASIC AUTH METHODS
# ==================

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
    data = {}
    count = db_session.query(func.count(Pages.id)).scalar()
    data['count'] = count
    return render_template('home.html', data=data )

@app.route('/save', methods=['POST'])
@requires_auth
def save():
    _json = request.get_json()
    pageNum = int(_json['pageNum'])
    new_contents = _json['contents']
    new_title = _json['title']
    app.logger.info(_json)
    page_to_update = Pages.query.get(pageNum)
    page_to_update.contents = new_contents
    page_to_update.title = new_title
    db_session.commit()
    return "OK", 200

@app.route('/new', methods=['GET'])
@requires_auth
def insert_new_page():
    db_session.add(Pages(contents='<p>This is a new page ready for editing</p>'))
    db_session.commit()
    count = db_session.query(func.count(Pages.id)).scalar()
    return str(count)

@app.route('/get', methods=['POST'])
@requires_auth
def get_page():
    _json = request.get_json()
    app.logger.info(_json)
    if _json is None:
        _json = {}
    data = {}
    pageId = int(_json['page'])
    if pageId is None:
        return 'invalid mime type?', 501
    excerpt = Pages.query.filter_by(id=pageId).first()
    if excerpt is None:
        return "ERROR", 202
    data['excerpt'] = excerpt.contents
    data['title'] = excerpt.title
    return jsonify(data), 200

# ==================
# ERROR HANDLER PAGE
# ==================

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return render_template('500.html'), 500


# ==================================
# after wsgi unload (server restart)
# ==================================

@app.teardown_appcontext
def shutdown_session(exception=None):
    app.logger.debug('teardown')
    db_session.remove()
