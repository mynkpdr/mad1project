from .main_routes import main_routes
from .auth_routes import auth_routes
from .admin_routes import admin_routes
from .professional_routes import professional_routes
from .customer_routes import customer_routes
from .api_routes import api_routes
from app.models.notification import Notification
from flask_login import current_user, LoginManager
from app.models.user import User


def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    app.register_blueprint(main_routes, url_prefix='/')
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(admin_routes, url_prefix='/admin')
    app.register_blueprint(professional_routes, url_prefix='/professional')
    app.register_blueprint(customer_routes, url_prefix='/')
    app.register_blueprint(api_routes, url_prefix='/api')

# This will be globally set
def register_global(app):
    @app.context_processor
    def inject_globals():
        return {
            'get_notifications': lambda: Notification.query.filter_by(is_read=False).order_by(Notification.date_created.desc()).filter_by(user_id=current_user.id).all()
        }

# register login manager
def register_login_manager(app):

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # User loader for Flask-Login
    @login_manager.user_loader
    def loader_user(user_id):
        # Retrieve the user by ID for session management
        return User.query.get(int(user_id))