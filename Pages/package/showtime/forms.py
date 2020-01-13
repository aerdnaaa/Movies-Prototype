from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateShowtime(FlaskForm):    
    theatre_name = SelectField(label="Theatre Name", choices=[])
    movie_title = SelectField(label="Movie Title", choices=[])
    timeslot = SelectMultipleField("Timeslot", choices=[])
    showtime_start_date = StringField(label="Showtime Start Date", validators=[DataRequired()])
    showtime_end_date = StringField(label="Showtime End Date", validators=[DataRequired()])
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
