from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateCarousel(FlaskForm):
    carousel_category = SelectField(label='Carousel Category', choices=[("movies","Movie"), ("promotion", "Promotion")])
    carousel_title = SelectMultipleField(label='Carousel Title', validators=[DataRequired()], choices=[])
    submit = SubmitField("Add carousel")         

class ModifyCarousel(FlaskForm):
    carousel_category = SelectField(label='Carousel Category', choices=[("movies","Movie"), ("promotion", "Promotion")])
    carousel_title = SelectMultipleField(label='Carousel Title', validators=[DataRequired()], choices=[])
    submit = SubmitField("Modify carousel")
