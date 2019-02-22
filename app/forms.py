from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, FormField, FieldList, HiddenField
from wtforms.validators import ValidationError, Email, EqualTo, Length
from app.models import User
from datetime import datetime


def _required(form, field):
    if not field.raw_data or not field.raw_data[0]:
        raise ValidationError("Field {} is required".format(field.description))


class EmbeddedForm:
    def __init__(self, *args, **kwargs):
        kwargs["meta"] = {"csrf": False}
        super(EmbeddedForm, self).__init__(*args, **kwargs)

class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))

class RemovableFieldList(FieldList):

    def remove(self, value):
        """ Removes the last entry from the list and returns it. """
        entry = self.entries.remove(value)
        self.last_index -= 1
        return entry

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


class SubgoalForm(EmbeddedForm, FlaskForm):
    id = HiddenField('Id')
    title = StringField('Title', validators=[_required, Length(1, 140)])
    duedate = NullableDateField('Due Date', format='%d.%m.%Y')
    delete_subgoal = SubmitField('Delete Subgoal')

    def validate_duedate(self, duedate):
        if duedate.data and duedate.data < datetime.utcnow().date():
            raise ValidationError('Please select DueDate >= today')

class GoalForm(FlaskForm):
    title = StringField('Title', validators=[_required, Length(1, 140)])
    description = TextAreaField('Description', validators=[Length(0, 1024)])
    duedate = NullableDateField('Due Date', format='%d.%m.%Y')
    subgoals = RemovableFieldList(FormField(SubgoalForm),
                         max_entries=100, label='Subgoals')
    add_subgoal = SubmitField('Add Subgoal')
    submit = SubmitField('Create')

    def validate_duedate(self, duedate):
        if duedate.data and duedate.data < datetime.utcnow().date():
            raise ValidationError('Please select DueDate >= today')
