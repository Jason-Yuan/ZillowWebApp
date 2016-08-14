import os
from datetime import datetime
from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from flask.ext.sqlalchemy import SQLAlchemy

# create a flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

# connect PostgreSQL with Flask app
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://boyuan:900109@localhost/buddy'

# associate Flask-Login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'landing.login'
login_manager.login_message = u'Please log in to explore more!'

# The user_loader callback only tells it how to reload the object for a user that has
# already been authenticated, such as when someone reconnects to a "remember me" session. 
@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# @app.before_request
# def before_request():
#     """Connect to the database before each request."""
#     g.db = models.DATABASE
#     g.db.connect()
#     g.user = current_user

# @app.after_request
# def after_request(response):
#     """Close the database connection after each request."""
#     g.db.close()
#     return response


# Views
from Buddy.views import landing, users, event
app.register_blueprint(landing.bp)
app.register_blueprint(users.bp)
app.register_blueprint(event.bp)

# Model
from Buddy.models import User
