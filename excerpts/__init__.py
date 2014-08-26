from flask import Flask, render_template
from database import db_session, init_db
from model.Pages import Pages

app = Flask(__name__)
init_db()

@app.route('/')
def hello():
    app.logger.debug(__path__)
    p = Pages(contents="It worked!")
    db_session.add(p)
    db_session.commit()
    return render_template('home.html')

@app.errorhandler(500)
def internal_error(exception):
    app.logger.exception(exception)
    return render_template('500.html'), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    app.logger.debug('teardown')
    db_session.remove()
