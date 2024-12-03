from app.models import db

# Professional Model
class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    service_price = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    experience = db.Column(db.Integer, default=0)
    documents = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0)

    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True)
    reviews = db.relationship('Review', backref='professional', lazy=True)