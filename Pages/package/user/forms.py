from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField,PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
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