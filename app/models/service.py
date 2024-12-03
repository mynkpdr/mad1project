from datetime import datetime
import pytz
from app.models import db

# Service Model
class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), default='service_default.png')
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True,)
    service_requests = db.relationship('ServiceRequest', backref='service', lazy=True)