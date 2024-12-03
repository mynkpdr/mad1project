from enum import Enum
from app.models import db
from datetime import datetime, timedelta
import pytz

# Enum for service request status
class ServiceStatus(Enum):
    REQUESTED = "REQUESTED"
    ASSIGNED = "ASSIGNED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"

# Service Request Model
class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'))
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))

    total_days = db.Column(db.Integer, nullable=False)
    hours_per_day = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)

    service_status = db.Column(db.Enum(ServiceStatus), default=ServiceStatus.REQUESTED)
    remarks = db.Column(db.Text)

    start_date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')) + timedelta(days=5), nullable=False) # 5 days from today
    date_of_completion = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
    date_updated = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))
