from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed

class ServiceForm(FlaskForm):
    name = StringField('Service Name*', validators=[DataRequired()])
    price = IntegerField('Base Price (₹)*', validators=[DataRequired()])
    category = SelectField('Category*', validators=[DataRequired()])
    image = FileField('Service Image (Under 1 MB)', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Service')

class CategoryForm(FlaskForm):
    name = StringField('Category Name*', validators=[DataRequired()])
    submit = SubmitField('Add Category')