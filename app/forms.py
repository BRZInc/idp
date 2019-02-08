from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField
from wtforms.validators import ValidationError, Email, EqualTo, Length
from app.models import User
from datetime import datetime


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError("Field {} is required".format(field.description))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[_required, Length(5, 64)])
    password = PasswordField('Password', validators=[_required, Length(5, 32)])
    remember_me = BooleanField('Remember Me', default=True)
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[_required, Length(5, 64)])
    firstname = StringField('First name', validators=[Length(0, 120)])
    lastname = StringField('Last name', validators=[Length(0, 120)])
    email = StringField('Email', validators=[
                        _required, Email(), Length(0, 120)])
    password = PasswordField('Password', validators=[_required, Length(5, 32)])
    password2 = PasswordField('Confirmation', validators=[
                              _required, EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please enter other username')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Please enter other email')


class GoalForm(FlaskForm):
    title = StringField('Title', validators=[_required, Length(1, 140)])
    description = TextAreaField('Description', validators=[Length(0, 1024)])
    duedate = DateField('Due Date', format='%d.%m.%y')
    submit = SubmitField('Create')

    def validate_duedate(self, duedate):
        if duedate.data and duedate.data < datetime.utcnow().date():
            raise ValidationError('Please select DueDate >= today')
