from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email

class CreateContactUsForm(FlaskForm):
    salutation = SelectField("Salutation", validators=[DataRequired()], choices=[("Mr","Mr"),("Mrs","Mrs"),("Ms","Ms"),("Dr","Dr")], default="Mr")
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    message = TextAreaField("Your message", validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField("Send Message")