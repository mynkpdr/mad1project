from flask_login import current_user
from app.models import User, Role
from flask import flash, redirect, url_for, request, jsonify, session, make_response
from functools import wraps
import jwt
from datetime import datetime, timedelta
import os
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Conflict, Unauthorized
import pytz

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User not authenticated", "danger")
            return redirect(url_for("main.index"))
        if current_user.role != Role.ADMIN:
            raise Forbidden
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User not authenticated", "danger")
            return redirect(url_for("main.index"))
        if current_user.role != Role.CUSTOMER:
            raise Forbidden
        return f(*args, **kwargs)
    return decorated_function

def professional_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("User not authenticated", "danger")
            return redirect(url_for("main.index"))
        if current_user.role != Role.PROFESSIONAL:
            raise Forbidden
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BadRequest as e:
            return jsonify({
                'success': False,
                'error': 'Bad Request',
        'message': e.description if e.description != "The browser (or proxy) sent a request that this server could not understand." else "Invalid request"
            }), 400
        except Unauthorized as e:
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': e.description if e.description != "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required." else "You are not authorized."
            }), 401
        except Forbidden as e:
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': e.description if e.description != "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server." else "You do not have access to this resource."
            }), 403
        except NotFound as e:
            return jsonify({
                'success': False,
                'error': 'Not Found',
        'message': e.description if e.description != "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again." else "The requested resource could not be found."
            }), 404
        except Conflict as e:
            return jsonify({
                'success': False,
                'error': 'Conflict',
        'message': e.description if e.description != "A conflict happened while processing the request. The resource might have been modified while the request was being processed." else "The data you are trying to submit conflicts with an existing resource."
            }), 409
        except KeyError as e:
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': f"Missing required field: {str(e)}" if str(e) else "Required field is missing"
            }), 400
        except TypeError as e:
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': f"Invalid data type: {str(e)}" if str(e) else "Invalid data type"
            }), 400
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': str(e) if str(e) else "Invalid value"
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': str(e) if str(e) else "An error occured"
            }), 500
    return decorated_function

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # Check token in session or Authorization header (for API calls)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        elif 'token' in request.headers:
            token = request.headers['token']
        elif 'token' in session:
            token = session['token']
        if not token:
            return f(c_user=None, *args, **kwargs)
        
        c_user = User.verify_jwt(token)
        if not c_user:
            return f(c_user=None, *args, **kwargs)
        # Check if the token is about to expire (within 5 minutes)
        payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        current_time = datetime.now(tz=pytz.timezone('Asia/Kolkata'))
        expiration_time = datetime.fromtimestamp(payload['exp'], tz=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
        if current_time >= expiration_time - timedelta(minutes=5):
            new_access_token = c_user.generate_jwt()    # Generate a new access token
            session['token'] = new_access_token  # Store the new token in the session
            response = make_response(f(c_user, *args, **kwargs))
            response.headers['Authorization'] = f"Bearer {new_access_token}"  # Return the new token in the response headers
            return response
        else:
            return f(c_user, *args, **kwargs)
    
    return decorated_function
