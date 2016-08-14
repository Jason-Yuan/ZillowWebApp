from flask import (Flask, Blueprint, g, render_template, flash, redirect, url_for,
                  abort)
from Buddy.models import User, create_user
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from Buddy import forms

bp = Blueprint('landing', __name__)


@bp.route('/')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    registerForm = forms.RegisterForm()
    if registerForm.validate_on_submit():
        flash("Yay, you registered!", "alert-success")
        create_user(
            username=registerForm.username.data,
            email=registerForm.email.data,
            password=registerForm.password.data
        )
        return redirect(url_for('users.profile'))
    return render_template('landing/index.html', registerForm=registerForm, loginForm=forms.LoginForm())


@bp.route('/login', methods=('GET', 'POST'))
def login():
    loginForm = forms.LoginForm()
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if not user:
            flash("Your email or password doesn't match!", "alert-danger")
        else:
            if check_password_hash(user.password, loginForm.password.data):
                login_user(user)
                flash("You've been logged in!", "alert-success")
                return redirect(url_for('event.explore'))
            else:
                flash("Your email or password doesn't match!", "alert-error")
    return render_template('landing/index.html', registerForm=forms.RegisterForm(), loginForm=loginForm)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "alert-info")
    return redirect(url_for('landing.register'))


# @bp.route('/new_post', methods=('GET', 'POST'))
# @login_required
# def post():
#     form = forms.PostForm()
#     if form.validate_on_submit():
#         Post.create(user=g.user.id,
#                            content=form.content.data.strip())
#         flash("Message posted! Thanks!", "alert-success")
#         return redirect(url_for('landing.index'))
#     return render_template('landing/post.html', form=form)


# @bp.route('/stream')
# @bp.route('/stream/<username>')
# def stream(username=None):
#     template = 'landing/stream.html'
#     if username and username != current_user.username:
#         try:
#             user = User.select().where(
#                 User.username**username).get()
#         except DoesNotExist:
#             abort(404)
#         else:
#             stream = user.posts.limit(100)
#     else:
#         stream = current_user.get_stream().limit(100)
#         user = current_user
#     if username:
#         template = 'landing/user_stream.html'
#     return render_template(template, stream=stream, user=user)


# @bp.route('/post/<int:post_id>')
# def view_post(post_id):
#     posts = Post.select().where(Post.id == post_id)
#     if posts.count() == 0:
#         abort(404)
#     return render_template('landing/stream.html', stream=posts)


# @bp.route('/follow/<username>')
# @login_required
# def follow(username):
#     try:
#         to_user = User.get(User.username**username)
#     except DoesNotExist:
#         abort(404)
#     else:
#         try:
#             Relationship.create(
#                 from_user=g.user._get_current_object(),
#                 to_user=to_user
#             )
#         except IntegrityError:
#             pass
#         else:
#             flash("You're now following {}!".format(to_user.username), "alert-success")
#     return redirect(url_for('landing.stream', username=to_user.username))

# @bp.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#     try:
#         to_user = User.get(User.username**username)
#     except DoesNotExist:
#         abort(404)
#     else:
#         try:
#             Relationship.get(
#                 from_user=g.user._get_current_object(),
#                 to_user=to_user
#             ).delete_instance()
#         except IntegrityError:
#             pass
#         else:
#             flash("You've unfollowed {}!".format(to_user.username), "alert-success")
#     return redirect(url_for('landing.stream', username=to_user.username))
