from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, IntegerField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired

class ServiceRequestForm(FlaskForm):
    category_id = SelectField('Category*', coerce=int, validators=[DataRequired()])
    service_id = SelectField('Service*', coerce=int, validators=[DataRequired()])
    customer_id = SelectField('Customer*', coerce=int, validators=[DataRequired()])
    professional_id = SelectField('Professional*', coerce=int, validators=[DataRequired()])
    start_date = DateField('Start Date*', format='%Y-%m-%d', validators=[DataRequired()])
    total_days = IntegerField('Total Number of Days*', validators=[DataRequired()])
    hours_per_day = IntegerField('Hours Per Day*', validators=[DataRequired()])
    remarks = TextAreaField('Remarks*', validators=[DataRequired()])
    cost = HiddenField('Cost', default=0)
    submit = SubmitField('Add Service Request')
