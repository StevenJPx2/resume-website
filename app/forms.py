from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    number = StringField('Phone Number')
    query = StringField('Enter your query here...', validators=[DataRequired()])
    submit = SubmitField('Send')