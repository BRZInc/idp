from app import db
from datetime import timedelta, datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	first_name = db.Column(db.String(120))
	last_name = db.Column(db.String(120))
	email = db.Column(db.String(120), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	goals = db.relationship('Goal', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {} id={}>'.format(self.username, self.id)

class Goal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(140), nullable=False)
	description = db.Column(db.String(1024))
	due_date = db.Column(db.DateTime, index=True, default=datetime.utcnow()+timedelta(days=30))
	created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow())
	updated_at = db.Column(db.DateTime, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return '<Goal {} id={}>'.format(self.title, self.id)