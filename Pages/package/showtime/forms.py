from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField,DateField
import shelve, datetime

def validate_start_date(form, field):
    today = datetime.date.today()
    if field.data != '':
        if datetime.datetime.strptime(field.data, "%Y-%m-%d").date() < today:
            raise ValidationError("Start date can start from today onwards")
def validate_end_date(form, field):
    if form.showtime_start_date.data != '' and field.data != '':
        start_date = datetime.datetime.strptime(form.showtime_start_date.data, "%Y-%m-%d").date()
        if datetime.datetime.strptime(field.data, "%Y-%m-%d").date() < start_date:
            raise ValidationError("End date must be after start date")

def validate_timeslot(form, field):  
    if field.data == []:
        raise ValidationError("Please choose a timeslot")

class CreateShowtime(FlaskForm):    
    theatre_name = SelectField(label="Theatre Name", choices=[])
    movie_title = SelectField(label="Movie Title", choices=[], validators=[DataRequired("Must select a movie")])
    timeslot = SelectMultipleField("Timeslot", choices=[], validators=[validate_timeslot])
    showtime_start_date = StringField(label="Showtime Start Date", validators=[DataRequired("Please choose a date"), validate_start_date])
    showtime_end_date = StringField(label="Showtime End Date", validators=[DataRequired("Please choose a date"), validate_end_date])
    hall_number = SelectField(label="Hall Number", choices=[])
    submit = SubmitField("Add Showtime")

class ModifyShowtime(FlaskForm):    
    theatre_name = SelectField(label="Theatre Name", choices=[])
    movie_title = SelectField(label="Movie Title", choices=[])
    timeslot = SelectMultipleField("Timeslot", choices=[], validators=[validate_timeslot])
    showtime_start_date = StringField(label="Showtime Start Date", validators=[DataRequired(), validate_start_date])
    showtime_end_date = StringField(label="Showtime End Date", validators=[DataRequired(), validate_end_date])
    hall_number = SelectField(label="Hall Number", choices=[])
    submit = SubmitField("Modify Showtime")

class PaymentForm(FlaskForm):
    fullName = StringField('Full Name',[validators.Length(min=1,max=150), validators.DataRequired(message="This cannot be empty!")])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email(message="Please enter valid email.")])
    dateOfBirth = DateField('Date of Birth', validators=[validators.DataRequired()], format="%Y-%m-%d",render_kw={"placeholder": "dd/mm/yyyy"})    
    gender = SelectField("Gender",validators=[DataRequired()],choices=[('Male','Male'),('Female','Female')])
    card_number = StringField('Card Number', [DataRequired()])
    name_on_card = StringField('Name on card', [DataRequired()],render_kw={"placeholder": "Name On Card"})
    dateOfExpiry = DateField('Date of Expiry', validators=[validators.DataRequired()], format="%Y-%m",render_kw={"placeholder": "MM/YYYY"})    
    cvc = StringField('CVC', [DataRequired(), Length(min=3, max=4, message="Not a valid CVC")],render_kw={"placeholder": "CVC"})
    submit = SubmitField('Pay Now')