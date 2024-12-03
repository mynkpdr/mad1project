from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Optional, NumberRange
from wtforms import TextAreaField, IntegerField, SubmitField

class ReviewForm(FlaskForm):
    professional_id = IntegerField('Professional ID*', validators=[DataRequired()])
    customer_id = IntegerField('Customer ID*', validators=[DataRequired()])
    service_request_id = IntegerField('Service Request ID*', validators=[DataRequired()])
    description = TextAreaField('Description*', validators=[Optional()])
    value = IntegerField('Value*', validators=[DataRequired(), NumberRange(min=1, max=5, message="Minimum 1 and Maximum 5 star rating allowed.")])
    submit = SubmitField('Add Review')