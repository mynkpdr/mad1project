from flask import request, jsonify, render_template

# Custom error handlers
def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 Bad Request errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Bad Request',
                'message': 'The request could not be understood or was missing required parameters.'
            }), 400
        return render_template('error/400.html', message=str(e)), 400

    @app.errorhandler(401)
    def unauthorized(e):
        """Handle 401 Unauthorized errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Unauthorized',
                'message': 'You are not authorized to access this resource. Please log in or provide valid credentials.'
            }), 401
        return render_template('error/401.html', message=str(e)), 401

    @app.errorhandler(403)
    def forbidden(e):
        """Handle 403 Forbidden errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Forbidden',
                'message': 'No Access'
            }), 403
        return render_template('error/403.html', message=str(e)), 403

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 Page Not Found errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Not Found',
                'message': 'The requested resource could not be found.'
            }), 404
        return render_template('error/404.html', message=str(e)), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handle 405 Method Not Allowed errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Method Not Allowed',
                'message': f"The HTTP method used is not allowed for the requested URL."
            }), 405
        return render_template('error/405.html', message=str(e)), 405

    @app.errorhandler(409)
    def conflict(e):
        """Handle 409 Conflict errors."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Conflict',
                'message': e.description
            }), 409
        raise Exception

    @app.errorhandler(415)
    def unsupported_media_type(e):
        """Handle 415 Unsupported Media Type Error."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Unsupported Media Type',
                'message': 'The server cannot process the media format of the request.'
            }), 415
        raise Exception

    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 Internal Server Error."""
        if request.path.startswith('/api/'):
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred. Our team has been notified.'
            }), 500
        return render_template('error/500.html', message='An unexpected error occurred.'), 500