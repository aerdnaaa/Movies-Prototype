from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

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