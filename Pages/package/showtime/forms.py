from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
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

class CreateShowtime(FlaskForm):    
    theatre_name = SelectField(label="Theatre Name", choices=[])
    movie_title = SelectField(label="Movie Title", choices=[])
    timeslot = SelectMultipleField("Timeslot", choices=[], validators=[DataRequired("Please choose a timeslot")])
    showtime_start_date = StringField(label="Showtime Start Date", validators=[DataRequired("Please choose a date"), validate_start_date])
    showtime_end_date = StringField(label="Showtime End Date", validators=[DataRequired("Please choose a date"), validate_end_date])
    hall_number = SelectField(label="Hall Number", choices=[])
    submit = SubmitField("Add Showtime")

class ModifyShowtime(FlaskForm):    
    theatre_name = SelectField(label="Theatre Name", choices=[])
    movie_title = SelectField(label="Movie Title", choices=[])
    timeslot = SelectMultipleField("Timeslot", choices=[])
    showtime_start_date = StringField(label="Showtime Start Date", validators=[DataRequired()])
    showtime_end_date = StringField(label="Showtime End Date", validators=[DataRequired()])
    hall_number = SelectField(label="Hall Number", choices=[])
    submit = SubmitField("Modify Showtime")
