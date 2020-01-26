from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField,DateField


class CreateUserForm(FlaskForm):
    fullName = StringField('Full Name',[validators.Length(min=1,max=150), validators.DataRequired(message="This cannot be empty!")])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email(message="Please enter valid email.")])
    dateOfBirth = DateField('Date of Birth', validators=[validators.DataRequired()], format="%Y-%m-%d",render_kw={"placeholder": "dd/mm/yyyy"})
    password = PasswordField('Password', [validators.length(min=8), validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password',[validators.length(min=8),validators.EqualTo('password', message='Passwords must match')])
    username = StringField('Username', [validators.length(min=2, max=20), validators.DataRequired()])
    gender = SelectField("Gender",validators=[DataRequired()],choices=[('Male','Male'),('Female','Female')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
     email = EmailField('Email', [Length(min=2, max=20, message="Character length does not fufil requirements"), DataRequired(message="Email cannot be empty")])
     password = PasswordField('Password', [DataRequired(message="Password cannot be empty")])
     login = SubmitField('Sign In')

class CreateAdminForm(FlaskForm):
    username = StringField("Username",[Length(min=1, max=30), DataRequired()], default="Admin")
    email = EmailField("Email", [DataRequired(), Email()])
    administrative_rights = SelectField("Administrative Rights", choices=[("Super Admin", "Super Admin"), ("Manage admins", "Manage admins"), ("Carousel", "Carousel")], default="Super Admin")    
    submit = SubmitField("Add Admin")

class ModifyAdminForm(FlaskForm):
    username = StringField("Username",[Length(min=1, max=30), DataRequired()], default="Admin")
    email = EmailField("Email", [DataRequired(), Email()])
    administrative_rights = SelectField("Administrative Rights", choices=[("Super Admin", "Super Admin"), ("Manage admins", "Manage admins"), ("Carousel", "Carousel")], default="Super Admin")    
    submit = SubmitField("Modify Admin")

    # username = StringField("Username",[Length(min=1, max=30), DataRequired()])
    # email = EmailField("Email", [DataRequired(), Email()])
    # password = PasswordField("Password", [Length(min=8), DataRequired()])
    # confirm_password = PasswordField("Confirm Password", [Length(min=8), DataRequired(), EqualTo('password', message="Passwords must match.")])        
    # submit = SubmitField("Modify Admin")