from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, EqualTo
from flask_wtf.file import FileAllowed

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[Optional()])
    pincode = StringField('Pin Code', validators=[Optional()])
    about = TextAreaField('About', validators=[Optional()])
    profile_image = FileField('Profile Image (Under 1 MB)', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[EqualTo('new_password', message='Passwords must match')])
    save = SubmitField('Save Changes')
