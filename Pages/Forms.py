# from wtforms import Form, StringField, SelectField, TextAreaField, validators, DateField, PasswordField
# from wtforms.fields.html5 import EmailField


# class CreateUserForm(Form):
#     firstName = StringField('First Name', [validators.Length(min=1,
#                                                              max=150), validators.DataRequired()])
#     lastName = StringField('Last Name', [validators.Length(min=1,
#                                                            max=150), validators.DataRequired()])
#     email = EmailField('Email address', [validators.DataRequired(), validators.Email])

#     DateofBirth = DateField('Date of Birth', validators=[validators.DataRequired()], format="%d/%m/%Y",
#                             render_kw={"placeholder": "dd/mm/yyyy"})

#     gender = SelectField('Gender', [validators.DataRequired()],
#                          choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
#                          default='')
#     remarks = TextAreaField('Remarks', [validators.Optional()])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirmpassword', message='Passwords must match')])
#     confirmpassword = PasswordField('Confirm Password')
#     Username = StringField('Username', [validators.length(min=1, max=30), validators.data_required])

#     def validate(self):
#         pass

# class loginform(Form):
#     username=StringField('',[validators.length(min=1,max=30),validators.input_required()],render_kw={"placeholder": "Username"})
#     password = PasswordField('', [validators.DataRequired()],render_kw={"placeholder": "Password"})

#     def validate(self):
#         pass

from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, IntegerField, TextAreaField, DateField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed

class CreateMovieTheatreForm(FlaskForm):
    theatre_name = StringField(label='Theatre Name', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_address = StringField(label='Theatre Address', validators=[DataRequired(), Length(min=3,max=20)])
    theatre_halls = IntegerField(label='Theatre Halls', validators=[DataRequired()])
    submit = SubmitField('Add Theatre')

class CreatePromotion(FlaskForm):
    promotion_title = StringField(label='Promotion Title', validators=[DataRequired(), Length(min=5, max=30)])
    promotion_description = TextAreaField(label='Promotion Description', validators=[DataRequired()])
    promotion_terms_and_condition = TextAreaField(label='Promotion Terms and Condition', validators=[DataRequired()])
    promotion_valid_start_date = StringField(label='Promotion Start Date', validators=[DataRequired()])
    promotion_valid_end_date = StringField(label='Promotion End Date', validators=[DataRequired()])    
    promotion_applicable_to = SelectField(label='Promotion Applicable To', validators=[DataRequired()], choices=[('All','All'),('Student','Student'),('Elderly','Elderly')], default='All')
    promotion_image = FileField(label='Promotion Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Add Promotion")

class ModifyPromotion(FlaskForm):
    promotion_title = StringField(label='Promotion Title', validators=[DataRequired(), Length(min=5, max=30)])
    promotion_description = TextAreaField(label='Promotion Description', validators=[DataRequired()])
    promotion_terms_and_condition = TextAreaField(label='Promotion Terms and Condition', validators=[DataRequired()])
    promotion_valid_start_date = StringField(label='Promotion Start Date', validators=[DataRequired()])
    promotion_valid_end_date = StringField(label='Promotion End Date', validators=[DataRequired()])    
    promotion_applicable_to = SelectField(label='Promotion Applicable To', validators=[DataRequired()], choices=[('All','All'),('Student','Student'),('Elderly','Elderly')], default='All')
    promotion_image = FileField(label='Promotion Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Modify Promotion")

class CreateCarousel(FlaskForm):
    carousel_title = StringField(label='Carousel Title', validators=[DataRequired(), Length(min=5, max=30)])
    carousel_category = SelectField(label='Carousel category', validators=[DataRequired()], choices=[('Nil','Nil'),('Movie','Movie'),('Rent Movie','Rent Movie'),('Promotion','Promotion')], default='Nil')
    carousel_image = FileField(label='Carousel Image', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField("Add carousel")

class CreateContactUsForm(FlaskForm):
    salutation = SelectField("Salutation", validators=[DataRequired()], choices=[("Mr","Mr"),("Mrs","Mrs"),("Ms","Ms"),("Dr","Dr")], default="Mr")
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    message = TextAreaField("Your message", validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField("Send Message")