from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateRental(FlaskForm):    
    movie_title = SelectField(label="Movie Title", choices=[("","")])
    rent_start_date = StringField(label="Rent Start Date", validators=[DataRequired()])
    rent_end_date = StringField(label="Rent End Date", validators=[DataRequired()])
    rent_price = IntegerField(label="Rent Price", validators=[DataRequired()])
    submit = SubmitField("Add Rental")

class ModifyRental(FlaskForm):    
    movie_title = SelectField(label="Movie Title", choices=[])
    rent_start_date = StringField(label="Rent Start Date", validators=[DataRequired()])
    rent_end_date = StringField(label="Rent End Date", validators=[DataRequired()])
    rent_price = IntegerField(label="Rent Price", validators=[DataRequired()])
    submit = SubmitField("Modify Rental")
