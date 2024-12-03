from flask_login import UserMixin
from enum import Enum
from app.models import db
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
bcrypt = Bcrypt()
import pytz
import os
import jwt
# Enum for user roles
class Role(Enum):
    ADMIN = "Admin"
    PROFESSIONAL = "Professional"
    CUSTOMER = "Customer"


# Unified User model
class User(db.Model, UserMixin):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    about = db.Column(db.String(500), default='')
    address = db.Column(db.String(200))
    pincode = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    profile_image = db.Column(db.String(200), default='default.jpg')
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    last_login = db.Column(db.DateTime)
    blocked = db.Column(db.Boolean, default=False)

    professional_data = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete')  # If a user has one professional
    customer_data = db.relationship('Customer', backref='user', uselist=False, cascade='all, delete')  # If a user has one customer

    def __init__(self, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_created = datetime.now(pytz.timezone('Asia/Kolkata'))   # Set the default date created to now irrespective of the user input
        self.set_password(password)  # Hash the password during user creation


    # Method to set the hashed password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Method to check if a password matches the stored hash
    def check_password(self, email, password):
        password_hash = User.query.filter_by(email=email).first().password
        return bcrypt.check_password_hash(password_hash, password)

    def generate_jwt(self):
        """Generates a JWT token for the user"""
        payload = {
            'user_id': self.id,
            'exp': datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(hours=12)  # Token expires in 12 hour
        }
        token = jwt.encode(payload, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
        return token

    @staticmethod
    def verify_jwt(token):
        """Verifies the JWT token and returns the user"""
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token