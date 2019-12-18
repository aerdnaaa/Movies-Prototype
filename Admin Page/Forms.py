from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class CreateMovieTheatreForm(FlaskForm):
    theatre_name = StringField(label='Theatre Name', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_address = StringField(label='Theatre Address', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_halls = IntegerField(label='Theatre Halls', validators=[DataRequired()])
    submit = SubmitField('Add Theatre')
