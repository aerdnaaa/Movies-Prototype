from flask_wtf import FlaskForm, Form
from flask_login import current_user
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField,DateField
import shelve, datetime

#! validation for CreateUserForm
def validate_email(form, field):
    #? checking if email is in shelve
    db = shelve.open('shelve.db', 'c')
    try:
        user_dict = db["Users"]
    except:
        user_dict = {}
        db["Users"] = user_dict
    db.close()
    print(user_dict)
    for user_class in user_dict.values():
        print(user_class.get_email())
        print(field.data)
        if user_class.get_email() == field.data:
            raise ValidationError("Email is already taken")
def validate_dateOfbirth(form, field):
    #? checking if date of birth is less than 14 years than today
    today_year = datetime.date.today().year
    if (today_year - field.data.year) < 14:
        raise ValidationError("You have not met age requirements of 14")

class CreateUserForm(FlaskForm):
    fullName = StringField('Full Name',[validators.Length(min=1,max=150), validators.DataRequired(message="This cannot be empty!")])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email(message="Please enter valid email."), validate_email])
    dateOfBirth = DateField('Date of Birth', validators=[validators.DataRequired(), validate_dateOfbirth], format="%Y-%m-%d",render_kw={"placeholder": "dd/mm/yyyy"})
    password = PasswordField('Password', [validators.length(min=8), validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password',[validators.length(min=8),validators.EqualTo('password', message='Passwords must match')])
    username = StringField('Username', [validators.length(min=2, max=20), validators.DataRequired()])
    gender = SelectField("Gender",validators=[DataRequired()],choices=[('Male','Male'),('Female','Female')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
     email = EmailField('Email address', [validators.DataRequired(), validators.Email(message="Please enter valid email.")])
     password = PasswordField('Password', validators=[DataRequired(message="Password cannot be empty")])
     rememberMe = BooleanField('Remember Me')
     login = SubmitField('Sign In')

class CreateAdminForm(FlaskForm):
    username = StringField("Username",[Length(min=1, max=30), DataRequired()], default="Admin")
    email = EmailField("Email", [DataRequired("Email is required "), Email(), validate_email])
    administrative_rights = SelectMultipleField("Administrative Rights", choices=[("Super Admin", "Super Admin"), ("Manage admins", "Manage admins"), ("Carousel", "Carousel")], default="Super Admin")    
    submit = SubmitField("Add Admin")

class ModifyAdminForm(FlaskForm):
    username = StringField("Username",[Length(min=1, max=30), DataRequired()], default="Admin")
    email = EmailField("Email", [DataRequired(), Email()])
    administrative_rights = SelectMultipleField("Administrative Rights", choices=[("Super Admin", "Super Admin"), ("Manage admins", "Manage admins"), ("Carousel", "Carousel")], default="Super Admin")    
    submit = SubmitField("Modify Admin")

class ModifyAdminAccount(FlaskForm):
    username = StringField("Username",[Length(min=1, max=30), DataRequired()])    
    new_password = PasswordField("Password", [Optional(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", [Length(min=8), EqualTo('new_password', message="Passwords must match."), Optional()]) 
    profile_picture = promotion_image = FileField(label='Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
    submit = SubmitField("Update")

class UpdateContactDetails(FlaskForm):
    fullName = StringField('Full Name',[validators.Length(min=1,max=150), validators.DataRequired(message="This cannot be empty!")])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email(message="Please enter valid email."), validate_email])
    dateOfBirth = DateField('Date of Birth', validators=[validators.DataRequired(),validate_dateOfbirth], format="%Y-%m-%d",render_kw={"placeholder": "dd/mm/yyyy"})
    username = StringField('Username', [validators.length(min=2, max=20), validators.DataRequired()])
    gender = SelectField("Gender",validators=[DataRequired()],choices=[('Male','Male'),('Female','Female')])
    submit = SubmitField('Save changes')
    
class UpdatePassword(FlaskForm):
    password = PasswordField('Password', [validators.length(min=8), validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password',[validators.length(min=8),validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Change Password')

class UpdateProfilePicture(FlaskForm):
    photo = FileField('Change Display Picture',validators=[FileRequired('File was empty!'),FileAllowed(['jpg','png'])])
    submit = SubmitField('Change Display Picture')
