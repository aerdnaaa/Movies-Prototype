from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CreateCarousel(FlaskForm):
    carousel_title = StringField(label='Carousel Title', validators=[DataRequired(), Length(min=5, max=30)])
    carousel_category = SelectField(label='Carousel category', validators=[DataRequired()], choices=[('Nil','Nil'),('Movie','Movie'),('Rent Movie','Rent Movie'),('Promotion','Promotion')], default='Nil')
    carousel_image = FileField(label='Carousel Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Add carousel")

class ModifyCarousel(FlaskForm):
    carousel_title = StringField(label='Carousel Title', validators=[DataRequired(), Length(min=5, max=30)])
    carousel_category = SelectField(label='Carousel category', validators=[DataRequired()], choices=[('Nil','Nil'),('Movie','Movie'),('Rent Movie','Rent Movie'),('Promotion','Promotion')], default='Nil')
    carousel_image = FileField(label='Carousel Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Modify carousel")