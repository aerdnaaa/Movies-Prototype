from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed

class CreateMovieTheatre(FlaskForm):
    theatre_name = StringField(label='Movie Theatre Name', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_image = FileField(label='Movie Theatre Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    theatre_halls = IntegerField(label='Movie Theatre Halls', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Add Movie Theatre')

class ModifyMovieTheatre(FlaskForm):
    theatre_name = StringField(label='Movie Theatre Name', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_image = FileField(label='Movie Theatre Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    theatre_halls = IntegerField(label='Movie Theatre Halls', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Modify Movie Theatre')
