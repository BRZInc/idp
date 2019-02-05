from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length
from app.models import User


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError("Field {} is required".format(field.name))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[_required, Length(5,64)])
    password = PasswordField('Password', validators=[_required, Length(5, 32)])
    remember_me = BooleanField('Remember Me', default=True)
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('First name')
    lastname = StringField('Last name')
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Password confirmation', validators=[
                              InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user is not None:
            raise ValidationError('Please enter other username')

    def validate_email(self, email):
        user = User.query.filter(User.email == email.data).first()
        if user is not None:
            raise ValidationError('Please enter other email')
