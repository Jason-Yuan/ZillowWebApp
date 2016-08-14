from flask import (Flask, Blueprint, g, render_template, flash, redirect, url_for,
                  abort)
from Buddy.models import User
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

bp = Blueprint('users', __name__)

@bp.route('/profile')
def profile():
	return render_template('users/profile.html')


@bp.route('/settings')
def settings():
	return render_template('users/setting.html')

@bp.route('/profile/edit')
def edit():
	return render_template('users/edit.html')

@bp.route('/notifications')
def notifications():
	return render_template('users/notifications.html')