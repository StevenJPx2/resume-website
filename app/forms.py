from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, MultipleFileField, SelectField, DateField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, URL

class ContactForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	number = StringField('Phone Number')
	query = TextAreaField('Enter your query here...', validators=[DataRequired()])
	submit = SubmitField('Send')
	
class LoginForm(UserMixin, FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Send')
	
class ProjectPostForm(FlaskForm):
	cover_img = FileField('Cover Image')
	imgs = MultipleFileField('Images')
	github_url = StringField('GitHub URL', validators=[URL()])
	title = StringField('Title', validators=[DataRequired()])
	body = TextAreaField('Body', validators=[DataRequired()])
	submit = SubmitField('Send')
 
	
class BlogPostForm(FlaskForm):
	cover_img = FileField('Cover Image')
	imgs = MultipleFileField('Images')
	title = StringField('Title', validators=[DataRequired()])
	body = TextAreaField('Body', validators=[DataRequired()])
	submit = SubmitField('Send')
 