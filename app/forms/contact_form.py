from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, TelField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    email = EmailField('Email address', validators=[DataRequired(), Email()], render_kw={"placeholder": "name@example.com"})
    phone = TelField('Phone Number', validators=[DataRequired()], render_kw={"placeholder": "Enter your phone number"})
    message = TextAreaField('Your Message', validators=[DataRequired()], render_kw={"placeholder": "Type your message here...", "rows": 4})
    submit = SubmitField('Send Message')