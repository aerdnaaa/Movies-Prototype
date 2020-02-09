from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
import shelve

def validate_movie_name(form,field):
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    db.close()
    for movie_title in Movies_dict.values():
        if movie_title.get_movie_name() == field.data:
            raise ValidationError("Movie Title Existed")

def validate_genre(form, field):
    if form.data == []:
        raise ValidationError("Genre must not be empty")

class CreateMovieForm(FlaskForm):            
        movie_name = StringField(label="Movie Name", validators=[DataRequired(message="Movie must have a name"), validate_movie_name])
        movie_poster = FileField(label="Movie Poster", validators=[DataRequired(message="Movie must have a poster"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
        movie_description = TextAreaField(label='Movie Description', validators=[DataRequired()])
        movie_genre = SelectMultipleField(label="Movie Genre", choices=[], validators=[validate_genre])
        movie_casts = TextAreaField(label="Movie Casts", validators=[DataRequired()])
        movie_director = StringField(label="Movie Director", validators=[DataRequired()])
        movie_fullvideo = FileField(label="Movie Full Video",validators=[DataRequired(message="This field is required to be filled in")])
        movie_trailer = FileField(label="Movie Trailer", validators=[DataRequired(message="This field is required to be filled in")])
        movie_duration = StringField(label="Movie Duration in Minutes", validators=[DataRequired()])
        movie_release_date = StringField(label="Movie Release Date", validators=[DataRequired()])
        movie_language = SelectField(label="Movie Language", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="English")
        movie_subtitles = SelectField(label="Movie Subtitles", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="Chinese")
        submit = SubmitField("Add Movies")                    

class ModifyMovieForm(FlaskForm):
        movie_name = StringField(label="Movie Name", validators=[DataRequired(message="Movie must have a name")])
        movie_poster = FileField(label="Movie Poster", validators=[DataRequired(message="Movie must have a poster"),FileAllowed(['jpg','png','jpeg'],message="This file type is not allowed")])
        movie_description = TextAreaField(label='Movie Description', validators=[DataRequired()])
        movie_genre = SelectMultipleField(label="Movie Genre", choices=[], validators=[validate_genre])
        movie_casts = TextAreaField(label="Movie Casts", validators=[DataRequired()])
        movie_director = StringField(label="Movie Director", validators=[DataRequired()])
        movie_fullvideo = FileField(label="Movie Full Video",validators=[DataRequired(message="movie must have a video"), FileAllowed(['mp4','mov'], message="This file type is not allowed")])
        movie_trailer = FileField(label="Movie Trailer", validators=[DataRequired(message="movie must have a video"), FileAllowed(['mp4','mov'], message="This file type is not allowed")])
        movie_duration = StringField(label="Movie Duration in Minutes", validators=[DataRequired()])
        movie_release_date = StringField(label="Movie Release Date", validators=[DataRequired()])
        movie_language = SelectField(label="Movie Language", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="English")
        movie_subtitles = SelectField(label="Movie Subtitles", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="Chinese")
        submit = SubmitField("Modify Movies")
