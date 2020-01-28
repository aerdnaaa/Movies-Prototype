from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateMovieForm(FlaskForm):
    movie_name = StringField(label="Movie Name", validators=[DataRequired()])
    movie_poster = FileField(label="Movie Poster", validators=[FileAllowed(['jpg','png','jpeg'])])
    movie_description = TextAreaField(label='Movie Description', validators=[DataRequired()])
    movie_genre = SelectMultipleField(label="Movie Genre", choices=[])
    movie_casts = TextAreaField(label="Movie Casts", validators=[DataRequired()])
    movie_director = StringField(label="Movie Director", validators=[DataRequired()])
    movie_fullvideo = FileField(label="Movie Full Video")
    movie_trailer = FileField(label="Movie Trailer") #, validators=[FileAllowed("mov", "mp4")]
    movie_duration = StringField(label="Movie Duration in Minutes", validators=[DataRequired()])
    movie_release_date = StringField(label="Movie Release Date", validators=[DataRequired()])
    movie_language = SelectField(label="Movie Language", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="English")
    movie_subtitles = SelectField(label="Movie Subtitles", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="Chinese")
    submit = SubmitField("Add Movies")

class ModifyMovieForm(FlaskForm):
    movie_name = StringField(label="Movie Name", validators=[DataRequired()])
    movie_poster = FileField(label="Movie Poster", validators=[FileAllowed(['jpg','png','jpeg'])])
    movie_description = TextAreaField(label='Movie Description', validators=[DataRequired()])
    movie_genre = SelectMultipleField(label="Movie Genre", choices=[])
    movie_casts = TextAreaField(label="Movie Casts", validators=[DataRequired()])
    movie_director = StringField(label="Movie Director", validators=[DataRequired()])
    movie_fullvideo = FileField(label="Movie Full Video")
    movie_trailer = FileField(label="Movie Trailer") #, validators=[FileAllowed("mov", "mp4")]
    movie_duration = StringField(label="Movie Duration in Minutes", validators=[DataRequired()])
    movie_release_date = StringField(label="Movie Release Date", validators=[DataRequired()])
    movie_language = SelectField(label="Movie Language", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="English")
    movie_subtitles = SelectField(label="Movie Subtitles", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="Chinese")
    submit = SubmitField("Modify Movies")
