"""database mod"""
import datetime

from flask.ext.bcrypt import generate_password_hash
from sqlalchemy.exc import IntegrityError
from Buddy import db

class User(db.Model):
	"""Flask-Login friendly User class
	   More: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
	"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(120))
	joined_at = db.Column(db.DateTime)
	is_admin = db.Column(db.Boolean)

	def __init__(self, username, email, password, joined_at=None, is_admin=False):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password)
		if joined_at == None:
			self.joined_at = datetime.datetime.now()
		self.is_admin = is_admin

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def __repr__(self):
		return '<User %s>' % self.username

def create_user(username, email, password, joined_at=None, is_admin=False):
	try:
		new_user = User(username, email, password, joined_at, is_admin)
		db.session.add(new_user)
		db.session.commit()
		return new_user
	except IntegrityError:
		raise ValueError("User already exists")



def initialize():
	print "Creating database tables..."
	db.create_all()
	print "Done!"