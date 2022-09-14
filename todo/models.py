from datetime import datetime
from todo import db,bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    todo = db.relationship('Todo', backref='owned_user', lazy=True)

    @property
    def password(self):
    	return self.password

    @password.setter
    def password(self,plain_password):
    	self.password_hash = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def check_password(self,logging_password):
    	return bcrypt.check_password_hash(self.password_hash,logging_password)


class Todo(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	content = db.Column(db.String(200),nullable=False)
	completed = db.Column(db.Integer,default=0)
	created_date = db.Column(db.DateTime,default=datetime.utcnow)
	user = db.Column(db.Integer(),db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Task %r>'%self.id