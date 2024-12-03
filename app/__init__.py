from flask import Flask
from app.config import config_options
from app.models import *
from app.routes import register_routes, register_global, register_login_manager
from app.errors import register_error_handlers
from app.utils.template_utils import register_template_filters
from flask_cors import CORS
from flask_migrate import Migrate
import os
from flasgger import Swagger
def create_app():
    app = Flask(__name__)
    app.config.from_object(config_options[os.getenv('FLASK_CONFIG', 'default')])

    register_routes(app)
    register_login_manager(app)
    register_global(app)
    register_error_handlers(app)
    register_template_filters(app)
    swagger = Swagger(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
        
    return app