from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# db = SQLAlchemy()

class User(UserMixin):
	def __init__(self, username, room):
		self.username = username
		self.room = room

	def get_id(self):
		return self.username + self.room
	# ''' User model '''
	# __tablename__ = "users"
	# id = db.Column(db.Integer, primary_key=True)
	# username = db.Column(db.String(25), unique=True, nullable=False)
	# password = db.Column(db.String(), nullable=False)

	# db.create_all()
