from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired

class CreateMovieForm(FlaskForm):            
        movie_name = StringField(label="Movie Name", validators=[DataRequired(message="Movie must have a name")])
        movie_poster = FileField(label="Movie Poster", validators=[DataRequired(message="Movie must have a poster"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
        movie_description = TextAreaField(label='Movie Description', validators=[DataRequired()])
        movie_genre = SelectMultipleField(label="Movie Genre", choices=[])
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
        movie_genre = SelectMultipleField(label="Movie Genre", choices=[])
        movie_casts = TextAreaField(label="Movie Casts", validators=[DataRequired()])
        movie_director = StringField(label="Movie Director", validators=[DataRequired()])
        movie_fullvideo = FileField(label="Movie Full Video",validators=[DataRequired(message="This field is required to be filled in"),FileAllowed("mov", "mp4")])
        movie_trailer = FileField(label="Movie Trailer", validators=[DataRequired(message="This field is required to be filled in"),FileAllowed("mov", "mp4")])
        movie_duration = StringField(label="Movie Duration in Minutes", validators=[DataRequired()])
        movie_release_date = StringField(label="Movie Release Date", validators=[DataRequired()])
        movie_language = SelectField(label="Movie Language", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="English")
        movie_subtitles = SelectField(label="Movie Subtitles", choices=[("English","English"), ("Chinese", "Chinese"), ("Arabic", "Arabic"), ("Korean", "Korean"), ("Japanese", "Japanese")], default="Chinese")
        submit = SubmitField("Modify Movies")
