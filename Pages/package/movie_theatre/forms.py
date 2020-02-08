from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from flask_wtf.file import FileField, FileAllowed
import shelve

def validate_theatre_name(form,field):
    db = shelve.open('shelve.db', 'c')
    try:
        Movie_theatre_dict = db["movie_theatre"]
    except:        
        Movie_theatre_dict = {}
        db["movie_theatre"] = Movie_theatre_dict
    db.close()
    for MT_name in Movie_theatre_dict.values():
        if MT_name.get_theatre_name() == field.data:
            raise ValidationError("Movie Theatre Name Existed")

class CreateMovieTheatre(FlaskForm):
    theatre_name = StringField(label='Movie Theatre Name', validators=[DataRequired(), Length(min=3,max=20), validate_theatre_name])
    # theatre_image = FileField(label='Movie Theatre Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    theatre_image = FileField(label='Movie Theatre Image', validators=[DataRequired(message="Movie Theatre must have an image"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
    theatre_halls = IntegerField(label='Movie Theatre Halls', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Add Movie Theatre')

class ModifyMovieTheatre(FlaskForm):
    theatre_name = StringField(label='Movie Theatre Name', validators=[DataRequired(), Length(min=3,max=20),])
    theatre_image = FileField(label='Movie Theatre Image', validators=[DataRequired(message="Movie Theatre must have an image"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
    theatre_halls = IntegerField(label='Movie Theatre Halls', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Modify Movie Theatre')
