from app.models import db
from datetime import datetime
import pytz


# Review Model
class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id', use_alter=True))
    description = db.Column(db.Text)
    value = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))
