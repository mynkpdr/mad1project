from flask import request, jsonify

from app.models import User
from app.utils.helpers import validate_fields
from werkzeug.exceptions import Forbidden, Unauthorized, NotFound


def get_jwt_token_controller():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    validate_fields(data, [
        ("email", str),
        ("password", str),
    ])
    
    user = User.query.filter_by(email=email).first()
    if user:
        if user.check_password(email, password):  # Ensure correct password
            if user.blocked:
                raise Forbidden("You are blocked. Contact us if this was a mistake.")
            elif user.professional_data and not user.professional_data.active:
                raise Forbidden("Document verification is pending. Please wait for admin approval.")
            # Create JWT token
            token = user.generate_jwt()
            # Return the JWT token in the response
            return (
                jsonify(
                    {
                        "success": True,
                        "token": token,
                        "message": "Logged in successfully.",
                    }
                ),
                200,
            )
        else:
            raise Unauthorized("Invalid email or password.")
    else:
        raise NotFound("Invalid email or password.")


# def refresh_jwt_token_controller():
#     refresh_token = request.json.get("refresh_token")
#     if not refresh_token:
#         raise Unauthorized("refresh_token is missing!")

#     try:
#         # Decode the refresh token to get the user_id
#         payload = jwt.decode(
#             refresh_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
#         )
#         user_id = payload["user_id"]

#         # Generate new access token
#         user = User.query.get(user_id)  # Retrieve the user from the database
#         new_access_token = user.generate_jwt()  # Generate a new JWT

#         response = jsonify({"success":True, "access_token": new_access_token, "message": "Refresh token generated successfully!"})
#         return response

#     except jwt.ExpiredSignatureError:
#         return jsonify({"success":False, "error": "JWT error", "message": "Refresh token has expired!"}), 401
#     except jwt.InvalidTokenError:
#         return jsonify({"success":False, "error": "JWT error", "message": "Invalid refresh token!"}), 401
