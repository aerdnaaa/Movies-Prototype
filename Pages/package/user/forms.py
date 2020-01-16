from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField,PasswordField
from wtforms.validators import DataRequired, Length, EqualTo,Email
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField,DateField


class CreateUserForm(FlaskForm):
    firstName = StringField('First Name',[validators.Length(min=1,max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    DateofBirth = DateField('Date of Birth', validators=[validators.DataRequired()], format="%Y-%m-%d",render_kw={"placeholder": "dd/mm/yyyy"})
    password = PasswordField('Password', [validators.length(min=8), validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password',[validators.length(min=8),validators.EqualTo('password', message='Passwords must match')])
    Username = StringField('Username', [validators.length(min=2, max=20), validators.DataRequired()])
    gender = SelectField(label="Gender",validators=[DataRequired()],choices=[('Male','Male'),('Female','Female')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
     Username = StringField('Username', [validators.length(min=2, max=20), validators.DataRequired()])
     password = PasswordField('Password', [validators.length(min=8), validators.DataRequired()])
     login = SubmitField('Login')