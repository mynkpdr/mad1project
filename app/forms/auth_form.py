from wtforms import StringField, PasswordField, EmailField, TelField, TextAreaField, BooleanField, SelectField, IntegerField, FileField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, NumberRange
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class BaseSignupForm(FlaskForm):
    name = StringField('Full Name*', validators=[DataRequired()])
    email = EmailField('Email*', validators=[DataRequired(), Email()])
    username = StringField('Username*', validators=[DataRequired(), Length(min=4)])
    phone = TelField('Phone*', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Optional()])
    pincode = IntegerField('Pincode*', validators=[
        DataRequired(),
        NumberRange(min=100000, max=999999, message="Pincode must be a 6-digit number")
    ])
    lat = StringField('Latitude')
    lng = StringField('Longitude')
    profile_image = FileField('Profile Image (Under 1 MB)*', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    password = PasswordField('Password*', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password*', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    terms = BooleanField('I agree to the Terms and Conditions*', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class CustomerSignupForm(BaseSignupForm):
    pass

class ProfessionalSignUpForm(BaseSignupForm):
    category = SelectField('Category*', validators=[DataRequired()])
    service_name = SelectField('Service Name*', validators=[DataRequired()])
    service_price = IntegerField('Price / Hour*', validators=[DataRequired()])
    experience = IntegerField('Experience (in Yrs.)', validators=[Optional()])
    documents = FileField('Documents (Aadhar Card, PAN Card)(Under 1 MB)*', validators=[DataRequired()])