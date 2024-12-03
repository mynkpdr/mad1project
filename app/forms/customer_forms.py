
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, FileField, TextAreaField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Email, Length, Optional, EqualTo, DataRequired, NumberRange
from flask_wtf.file import FileAllowed

class EditCustomerPersonalForm(FlaskForm):
    name = StringField('Name*', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email*', validators=[DataRequired(), Email(), Length(max=100)])
    phone = StringField('Phone*', validators=[DataRequired(), Length(max=15)])
    username = StringField('Username*', validators=[DataRequired(), Length(max=50)])
    about = StringField('About', validators=[Length(max=500), Optional()])
    profile_image = FileField('Profile Image (Under 1 MB)', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')

class EditCustomerAddressForm(FlaskForm):
    address = TextAreaField('Address', validators=[Length(max=200), Optional()])
    pincode = IntegerField('Pincode*', validators=[
        DataRequired(),
        NumberRange(min=100000, max=999999, message="Pincode must be a 6-digit number")
    ])
    lat = StringField('Latitude')
    lng = StringField('Longitude')
    submit = SubmitField('Save Changes')

class EditCustomerSecurityForm(FlaskForm):
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Length(min=8)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change Password')
