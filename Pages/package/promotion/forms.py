from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
import shelve, datetime

def validate_promotion_title(form, field):
    db = shelve.open('shelve.db', 'c')
    try:
        Promotion_dict = db["promotion"]
    except:
        Promotion_dict = {}
        db["promotion"] = Promotion_dict
    db.close()
    for promo_title in Promotion_dict.values():
        if promo_title.get_title() == field.data:
            raise ValidationError("Promotion Title Existed")

def validate_start_date(form, field):
    today = datetime.date.today()
    if field.data != '':
        if datetime.datetime.strptime(field.data, "%Y-%m-%d").date() < today:
            raise ValidationError("Start date can start from today onwards")

def validate_end_date(form, field):
    if form.promotion_valid_end_date.data != '' and field.data != '':
        start_date = datetime.datetime.strptime(form.promotion_valid_start_date.data, "%Y-%m-%d").date()
        if datetime.datetime.strptime(field.data, "%Y-%m-%d").date() < start_date:
            raise ValidationError("End date must be after start date")

class CreatePromotion(FlaskForm):
    promotion_title = StringField(label='Promotion Title', validators=[DataRequired(message="Promotion title is required"), validate_promotion_title, Length(min=5, max=30)])
    promotion_description = TextAreaField(label='Promotion Description', validators=[DataRequired(message="Description is required")])
    promotion_terms_and_condition = TextAreaField(label='Promotion Terms and Condition', validators=[DataRequired(message="Terms & Condition is required")])
    promotion_promoPrice = StringField(label='Promo Price', validators=[DataRequired()])
    promotion_valid_start_date = StringField(label='Promotion Start Date', validators=[DataRequired(message="Start Date is required"), validate_start_date])
    promotion_valid_end_date = StringField(label='Promotion End Date', validators=[DataRequired("End Date is required"), validate_end_date])    
    promotion_applicable_to = SelectField(label='Promotion Applicable To', validators=[DataRequired()], choices=[('All','All'),('Student','Student'),('Elderly','Elderly')], default='All')
    promotion_image = FileField(label='Promotion Image', validators=[DataRequired(message="Promotion must have a poster"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
    submit = SubmitField("Add Promotion")

class ModifyPromotion(FlaskForm):
    promotion_title = StringField(label='Promotion Title', validators=[DataRequired(message="Promotion title is required"), Length(min=5, max=30),])
    promotion_description = TextAreaField(label='Promotion Description', validators=[DataRequired(message="Description is required")])
    promotion_terms_and_condition = TextAreaField(label='Promotion Terms and Condition', validators=[DataRequired(message="Terms & Condition is required")])
    promotion_promoPrice = StringField(label='Promo Price', validators=[DataRequired()])
    promotion_valid_start_date = StringField(label='Promotion Start Date', validators=[DataRequired(message="Start Date is required"), validate_start_date])
    promotion_valid_end_date = StringField(label='Promotion End Date', validators=[DataRequired("End Date is required"), validate_end_date])    
    promotion_applicable_to = SelectField(label='Promotion Applicable To', validators=[DataRequired()], choices=[('All','All'),('Student','Student'),('Elderly','Elderly')], default='All')
    promotion_image = FileField(label='Promotion Image', validators=[DataRequired(message="Promotion must have a poster"), FileAllowed(['jpg','png','jpeg'], message="This file type is not allowed")])
    submit = SubmitField("Modify Promotion")