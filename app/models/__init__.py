from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, Role  
from .customer import Customer  
from .professional import Professional  
from .service import Service  
from .service_request import ServiceRequest, ServiceStatus  
from .review import Review  
from .contact import Contact  
from .contact import Contact  
from .notification import Notification  
from .category import Category