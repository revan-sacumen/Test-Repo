from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
from todo.models import *

class RegisterForm(FlaskForm):
	def validate_username(self,instance_username):
		username_obj = User.query.filter_by(username=instance_username.data).first()
		if username_obj:
			raise ValidationError("Username already Exists Please Try diffrent username!!")
	def validate_email_address(self,instance_mail):
		email_obj = User.query.filter_by(email_address=instance_mail.data).first()
		if email_obj:
			raise ValidationError("Email already Exists Try diffrent Email!!")

	username = StringField(label="User Name",validators=[Length(min=2,max=6),DataRequired()])
	email_address = StringField(label="Email",validators=[Email(),DataRequired()])
	password = PasswordField(label="Password",validators=[Length(min=6),DataRequired()])
	confirm_password = PasswordField(label="Confirm Password",validators=[EqualTo("password"),DataRequired()]) 
	submit = SubmitField(label="Create Account") 

class LoginForm(FlaskForm):
	username = StringField(label="User Name",validators=[DataRequired()])
	password = PasswordField(label="Password",validators=[DataRequired()])
	submit = SubmitField(label="Login") 