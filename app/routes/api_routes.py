import os
import jwt

from flask import Blueprint, session
from app.controllers.service import *
from app.controllers.contact import *
from app.controllers.review import *
from app.controllers.service_request import *
from app.controllers.notification import *
from app.controllers.token import *
from app.controllers.category import *
from app.controllers.professional import *
from app.controllers.customer import *
from app.controllers.user import *
from app.utils.file_utils import FileUtils
from app.decorators import jwt_required, handle_errors
from app.models import Role
from werkzeug.exceptions import Forbidden
from flasgger import swag_from
from app.swagger.review import *
from app.swagger.service import *
from app.swagger.contact import *
from app.swagger.category import *
from app.swagger.service_request import *
from app.swagger.notification import *
from app.swagger.customer import *
from app.swagger.professional import *
from app.swagger.user import *
from app.swagger.token import *
from app.swagger.search import *
api_routes = Blueprint("api", __name__)



@api_routes.route('/reviews', methods=['GET'])
@jwt_required
@handle_errors
@swag_from(get_reviews_dict)
def get_reviews(c_user):
    if c_user:
        if c_user.role == Role.PROFESSIONAL:
            return get_reviews_controller(c_user=c_user)
        elif c_user.role == Role.CUSTOMER:
            return get_reviews_controller(c_user=c_user)
        elif c_user.role == Role.ADMIN:
            return get_reviews_controller()
    else:
        raise Forbidden


@api_routes.route('/reviews', methods=['POST'])
@jwt_required
@handle_errors
@swag_from(create_review_dict)
def create_review(c_user):
    if c_user:
        if c_user.role == Role.CUSTOMER:
            return create_review_controller(c_user=c_user)
        elif c_user.role == Role.ADMIN:
            return create_review_controller()
        else:
            raise Forbidden
    else:
        raise Forbidden

@api_routes.route('/review/<int:id>', methods=['DELETE'])
@jwt_required
@handle_errors
@swag_from(delete_review_dict)
def review(c_user, id):
    if c_user:
        if c_user.role == Role.CUSTOMER:
            return delete_review_controller(c_user=c_user, review_id=id)
        elif c_user.role == Role.ADMIN:
            return delete_review_controller(review_id=id)
    else:
        raise Forbidden


@api_routes.route("/services", methods=["GET"])
@handle_errors
@swag_from(get_services_dict)
def get_services():
    return get_services_controller()


@api_routes.route("/services", methods=["POST"])
@jwt_required
@handle_errors
@swag_from(create_service_dict)
def create_service(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return create_service_controller()
    else:
        return Forbidden


@api_routes.route("/service/<int:id>", methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_service_dict)
def edit_service(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return edit_service_controller(id)
    else:
        raise Forbidden


@api_routes.route("/service/<int:id>", methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_service_dict)
def delete_service(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return delete_service_controller(id)
    else:
        raise Forbidden


@api_routes.route("/service/<int:id>", methods=["GET"])
@handle_errors
@swag_from(get_service_dict)
def get_service(id):
    return get_service_controller(id)


@api_routes.route('/categories', methods=["POST"])
@jwt_required
@handle_errors
@swag_from(create_category_dict)
def create_category(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return create_category_controller()
    else:
        raise Forbidden

@api_routes.route('/categories', methods=["GET"])
@handle_errors
@swag_from(get_categories_dict)
def get_categories():
    return get_categories_controller()


@api_routes.route('/category/<int:id>', methods=["GET"])
@handle_errors
@swag_from(get_category_dict)
def get_category(id):
    return get_category_controller(id)


@api_routes.route('/category/<int:id>', methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_category_dict)
def delete_category(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return delete_category_controller(id)
    else:
        raise Forbidden


@api_routes.route('/category/<int:id>', methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_category_dict)
def edit_category(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return edit_category_controller(id)
    else:
        raise Forbidden



@api_routes.route('/category/<int:id>/services', methods=["GET"])
@handle_errors
@swag_from(get_category_services_dict)
def get_category_services(id):
    return get_category_services_controller(id)


@api_routes.route("/contacts", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_contacts_dict)
def get_contacts(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return get_contacts_controller()
    else:
        raise Forbidden

@api_routes.route("/contacts", methods=["POST"])
@handle_errors
@swag_from(create_contact_dict)
def create_contact():
    return create_contact_controller()


@api_routes.route("/contact/<int:id>", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_contact_dict)
def get_contact(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return get_contact_controller(id)
    else:
        raise Forbidden


@api_routes.route("/contact/<int:id>", methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_contact_dict)
def delete_contact(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return delete_contact_controller(id)
    else:
        raise Forbidden


@api_routes.route("/service/<int:id>/category", methods=["GET"])
@handle_errors
@swag_from(get_service_category_dict)
def get_service_category(id):
    return get_service_category_controller(id)


@api_routes.route("/service/<int:id>/service_requests", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_service_service_requests_dict)
def get_service_service_requests(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return get_service_service_requests_controller(id)
    else:
        raise Forbidden



@api_routes.route('/service/<int:id>/nearby_professionals', methods=['POST'])
@jwt_required
@handle_errors
@swag_from(get_nearby_professionals_dict)
def nearby_professionals(c_user, id):
    if c_user and c_user.role == Role.CUSTOMER:
        return get_nearby_professionals_controller(c_user=c_user, service_id=id)
    else:
        raise Forbidden

@api_routes.route('/service/<int:id>/pincode_professionals', methods=['POST'])
@jwt_required
@handle_errors
@swag_from(get_pincode_professionals_dict)
def pincode_professionals(c_user, id):
    if c_user and c_user.role == Role.CUSTOMER:
        return get_pincode_professionals_controller(service_id=id)
    else:
        raise Forbidden


@api_routes.route("/service_requests", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_service_requests_dict)
def get_service_requests(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return get_service_requests_controller()
    elif c_user and c_user.role == Role.PROFESSIONAL:
        return get_service_requests_controller(c_user=c_user)
    elif c_user and c_user.role == Role.CUSTOMER:
        return get_service_requests_controller(c_user=c_user)
    else:
        raise Forbidden


@api_routes.route("/service_requests", methods=["POST"])
@jwt_required
@handle_errors
@swag_from(create_service_request_dict)
def create_service_request(c_user):
    if c_user and c_user.role == Role.CUSTOMER:
        return create_service_request_controller(c_user=c_user)
    elif c_user and c_user.role == Role.ADMIN:
        return create_service_request_controller()
    else:
        raise Forbidden


@api_routes.route("/service_request/<int:id>", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_service_request_dict)
def get_service_request(c_user, id):
    if c_user:
        if c_user.role == Role.ADMIN:
            return get_service_request_controller(service_request_id=id)
        elif c_user.role == Role.CUSTOMER:
            return get_service_request_controller(service_request_id=id, c_user=c_user)
        elif c_user.role == Role.PROFESSIONAL:
            return get_service_request_controller(service_request_id=id, c_user=c_user)
    else:
        raise Forbidden

@api_routes.route("/service_request/<int:id>", methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_service_request_dict)
def edit_service_request(c_user, id):
    if c_user:
        if c_user.role == Role.ADMIN:
            return edit_service_request_controller(service_request_id=id)
        elif c_user.role == Role.CUSTOMER:
            return edit_service_request_controller(service_request_id=id, c_user=c_user)
        elif c_user.role == Role.PROFESSIONAL:
            return edit_service_request_controller(service_request_id=id, c_user=c_user)
    else:
        raise Forbidden


@api_routes.route("/service_request/<int:id>", methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_service_request_dict)
def delete_service_request(c_user, id):
    if c_user:
        if c_user.role == Role.ADMIN:
                return delete_service_request_controller(service_request_id=id)
        else:
            raise Forbidden
    else:
        raise Forbidden


@api_routes.route("/notifications", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_notifications_dict)
def get_notifications(c_user):
    if c_user:
        return get_notifications_controller(c_user)
    else:
        raise Forbidden

@api_routes.route("/notifications", methods=["POST"])
@jwt_required
@handle_errors
@swag_from(create_notification_dict)
def create_notification(c_user):
    if c_user:
        if c_user.role == Role.ADMIN:
            return create_notification_controller()
        else:
            raise Forbidden
    else:
        raise Forbidden

@api_routes.route("/notification/<int:id>", methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_notification_dict)
def get_notification(c_user, id):
    notification = Notification.query.get(id)
    if not notification:
        raise NotFound(f"Notification with ID {id} not found.")
    if c_user:
        if (c_user.role == Role.ADMIN) or (notification.user_id == c_user.id):
            return get_notification_controller(id)
        else:
            raise Forbidden
    else:
        raise Forbidden

@api_routes.route("/notification/<int:id>", methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_notification_dict)
def edit_notification(c_user, id):
    notification = Notification.query.get(id)
    if not notification:
        raise NotFound(f"Notification with ID {id} not found.")
    if c_user:
        if (c_user.role == Role.ADMIN) or (notification.user_id == c_user.id):
            return edit_notification_controller(id)
        else:
            raise Forbidden
    else:
        raise Forbidden


@api_routes.route("/notification/<int:id>", methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_notification_dict)
def delete_notification(c_user, id):
    notification = Notification.query.get(id)
    if not notification:
        raise NotFound(f"Notification with ID {id} not found.")
    if c_user:
        if (c_user.role == Role.ADMIN) or (notification.user_id == c_user.id):
            return delete_notification_controller(id)
        else:
            raise Forbidden
    else:
        raise Forbidden


@api_routes.route("/notification/<int:id>/read", methods=["POST"])
@jwt_required
@handle_errors
@swag_from(read_notification_dict)
def read_notification(c_user, id):
    return read_notification_controller(c_user=c_user, notification_id=id)


@api_routes.route('/customers', methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_customers_dict)
def get_customers(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return get_customers_controller()
    else:
        raise Forbidden



@api_routes.route('/customers', methods=["POST"])
@handle_errors
@swag_from(create_customer_dict)
def create_customer():
    return create_customer_controller()


@api_routes.route('/customer/<int:id>/summary')
@jwt_required
@handle_errors
@swag_from(get_customer_summary_dict)
def get_customer_summary(c_user, id):
    if c_user and c_user.role == Role.CUSTOMER and c_user.customer_data.id == id:  
        return get_customer_summary_controller(customer_id=id, c_user=c_user)
    elif c_user and c_user.role == Role.ADMIN:
        return get_customer_summary_controller(customer_id=id)
    else:
        raise Forbidden



@api_routes.route('/customer/<int:id>', methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_customer_dict)
def get_customer(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return get_customer_controller(customer_id=id)
    elif c_user and c_user.role == Role.CUSTOMER:
        return get_customer_controller(customer_id=id, c_user=c_user)
    else:
        raise Forbidden


@api_routes.route('/customer/<int:id>', methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_customer_dict)
def edit_customer(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return edit_customer_controller(customer_id=id)
    elif c_user and c_user.role == Role.CUSTOMER:
        return edit_customer_controller(customer_id=id, c_user=c_user)
    else:
        raise Forbidden


@api_routes.route('/customer/<int:id>', methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_customer_dict)
def delete_customer(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return delete_customer_controller(customer_id=id)
    else:
        raise Forbidden

@api_routes.route('/customer/<int:id>/profile')
@handle_errors
@swag_from(get_customer_profile_dict)
def get_customer_profile(id):
    return get_customer_profile_controller(customer_id=id)

@api_routes.route('/customer/<int:id>/block', methods=["POST"])
@jwt_required
@handle_errors
@swag_from(block_customer_dict)
def block_customer(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return block_customer_controller(customer_id=id)
    else:
        raise Forbidden

@api_routes.route('/professionals', methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_professionals_dict)
def get_professionals(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return get_professionals_controller()
    else:
        raise Forbidden

@api_routes.route('/professionals', methods=["POST"])
@handle_errors
@swag_from(create_professional_dict)
def create_professional():
        return create_professional_controller()

@api_routes.route('/professional/<int:id>', methods=["GET"])
@jwt_required
@handle_errors
@swag_from(get_professional_dict)
def get_professional(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return get_professional_controller(professional_id=id)
    elif c_user and c_user.role == Role.PROFESSIONAL:
        return get_professional_controller(professional_id=id, c_user=c_user)
    else:
        raise Forbidden


@api_routes.route('/professional/<int:id>', methods=["DELETE"])
@jwt_required
@handle_errors
@swag_from(delete_professional_dict)
def delete_professional(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return delete_professional_controller(professional_id=id)
    else:
        raise Forbidden


@api_routes.route('/professional/<int:id>', methods=["PUT"])
@jwt_required
@handle_errors
@swag_from(edit_professional_dict)
def edit_professional(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return edit_professional_controller(professional_id=id)
    elif c_user and c_user.role == Role.PROFESSIONAL:
        return edit_professional_controller(professional_id=id, c_user=c_user)
    else:
        raise Forbidden


@api_routes.route('/professional/<int:id>/summary')
@jwt_required
@handle_errors
@swag_from(get_professional_summary_dict)
def get_professional_summary(c_user, id):
    if c_user and c_user.role == Role.PROFESSIONAL and c_user.professional_data.id == id:  
        return get_professional_summary_controller(professional_id=id, c_user=c_user)
    elif c_user and c_user.role == Role.ADMIN:
        return get_professional_summary_controller(professional_id=id)
    else:
        raise Forbidden
    
@api_routes.route('/professional/<int:id>/active', methods=["POST"])
@jwt_required
@handle_errors
@swag_from(active_professional_dict)
def active_professional(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return active_professional_controller(professional_id=id)
    else:
        raise Forbidden
    
@api_routes.route('/professional/<int:id>/block', methods=["POST"])
@jwt_required
@handle_errors
@swag_from(block_professional_dict)
def block_professional(c_user, id):
    if c_user and c_user.role == Role.ADMIN:
        return block_professional_controller(professional_id=id)
    else:
        raise Forbidden

@api_routes.route('/professional/<int:id>/profile')
@handle_errors
@swag_from(get_professional_profile_dict)
def get_professional_profile(id):
    return get_professional_profile_controller(professional_id=id)


@api_routes.route('/users')
@jwt_required
@handle_errors
@swag_from(get_users_dict)
def get_users(c_user):
    if c_user and c_user.role == Role.ADMIN:
        return get_users_controller()
    else:
        raise Forbidden


@api_routes.route("/search")
@jwt_required
@handle_errors
@swag_from(search_dict)
def search(c_user):
    query = request.args.get('q')
    if not query and query != "":
        return jsonify({"message": "No search query provided", "results": []}), 400
    type = request.args.get("t")
    if not type:
        return jsonify({"message": "No search type provided", "results": []}), 400

    if c_user and c_user.role == Role.ADMIN:
        if type == "service_request":
            return search_service_requests_controller()
        elif type == "service":
            return search_service_controller()
        elif type == "category":
            return search_category_controller()
        elif type == "message":
            return search_contacts_controller()
        elif type == "user":
            return search_users_controller()
        elif type == "professional":
            return search_profesionals_controller()
        elif type == "customer":
            return search_customers_controller()
        else:
            return jsonify({"message": "Invalid search type provided", "results": []}), 400
    elif c_user:
        if type == "service_request":
            return search_service_requests_controller(c_user=c_user)
        elif type == "service":
            return search_service_controller()
        else:
            return jsonify({"message": "Invalid search type provided", "results": []}), 400
    else:
        if type == "service":
            return search_service_controller()
        else:
            return jsonify({"message": "Invalid search type provided", "results": []}), 400

upload_image_dict = {
    "summary": "Upload an image or document.",
    "description": "Upload an image or document.",
    "operationId": "upload_controller",
    "tags": [
        "Upload"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "requestBody": {
                    "required": True,
                    "content": {
                        "multipart/form-data": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "image": {
                                        "type": "string",
                                        "format": "binary",
                                        "description": "Image file to upload."
                                    },
                                    "document": {
                                        "type": "string",
                                        "format": "binary",
                                        "description": "Document file to upload."
                                    },
                                    "service": {
                                        "type": "string",
                                        "format": "binary",
                                        "description": "Service image file to upload."
                                    }
                                }
                            }
                        }
                    }
                },
                "responses" : {
                    "201" : {
                        "description": "Image or document uploaded successfully with filename",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                            "example": True
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "File uploaded successfully"
                                        },
                                        "filename": {
                                            "type": "string",
                                            "example": "document_12345.pdf"
                                        }
                                    }
                                }
                            }
                        }
                    },
                }
}

@api_routes.route("/upload", methods=["POST"])
@handle_errors
@swag_from(upload_image_dict)
def upload_image():
    if "image" not in request.files and "document" not in request.files and "service" not in request.files:
        return jsonify(success=False, message="No file part"), 400
    if "document" in request.files:
        document = request.files["document"]
        if document and FileUtils.allowed_file(document.filename):
            if FileUtils.is_file_size_allowed(document):
                filename = FileUtils.get_unique_filename(document.filename)
                filepath = os.path.join(os.getenv('PROFESSIONAL_DOCUMENT_UPLOAD_FOLDER'), filename)
                if not os.path.exists(os.getenv('PROFESSIONAL_DOCUMENT_UPLOAD_FOLDER')):
                    os.makedirs(os.getenv('PROFESSIONAL_DOCUMENT_UPLOAD_FOLDER'))
                document.save(filepath)
                return (
                    jsonify(
                        success=True, message="File uploaded successfully", filename=filename
                    ),
                    201,
                )
            else:
                return jsonify(success=False, message="The document should be under 1 MB"), 400
        else:
            return jsonify(success=False, message="Invalid file type"), 400
    elif "image" in request.files:
        image = request.files["image"]

        if image and FileUtils.allowed_file_image(image.filename):
            if FileUtils.is_file_size_allowed(image):
                filename = FileUtils.get_unique_filename(image.filename)  # Secure the filename
                filepath = os.path.join(os.getenv("PROFILE_IMAGE_UPLOAD_FOLDER"), filename)
                image.save(filepath)  # Save the image
                return (
                    jsonify(
                        success=True, message="Image uploaded successfully", filename=filename
                    ),
                    201,
                )
            else:
                return jsonify(success=False, message="The image should be under 1 MB"), 400
        else:
            return jsonify(success=False, message="Invalid file type"), 400
    elif "service" in request.files:
        serviceimage = request.files["service"]

        if serviceimage and FileUtils.allowed_file_image(serviceimage.filename):
            if FileUtils.is_file_size_allowed(serviceimage):
                filename = FileUtils.get_unique_filename(serviceimage.filename)  # Secure the filename
                filepath = os.path.join(os.getenv("SERVICE_IMAGE_UPLOAD_FOLDER"), filename)
                serviceimage.save(filepath)  # Save the file
                return (
                    jsonify(
                        success=True, message="Image uploaded successfully", filename=filename
                    ),
                    201,
                )
            else:
                return jsonify(success=False, message="The service image should be under 1 MB"), 400
        return jsonify(success=False, message="Invalid file type"), 400


@api_routes.route("/gettoken", methods=["POST"])
@handle_errors
@swag_from(get_jwt_token_dict)
def get_jwt_token():
    return get_jwt_token_controller()


# @api_routes.route("/refreshtoken", methods=["POST"])
# @handle_errors
# @swag_from()
# def refreshtoken():
#     return refresh_jwt_token_controller()


@api_routes.route("/me")
def me():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    elif 'token' in request.headers:
        token = request.headers['token']
    elif 'token' in session:
        token = session['token']
    if not token:
        return jsonify({"token":None, "success":False, "message":"Token neededd"})
    c_user = User.verify_jwt(token)
    if not c_user:
        return jsonify({"token":None, "success":False, "message":"User not found"})
    
    payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    role = None
    if c_user.role == Role.CUSTOMER:
        role = "customer"
    elif c_user.role == Role.PROFESSIONAL:
        role = "professional"
    elif c_user.role == Role.ADMIN:
        role = "admin"
    
    return ({
        "token":token,
        "role":role,
        "name":c_user.name,
        "email":c_user.email,
        "id":c_user.customer_data.id if c_user.customer_data else c_user.professional_data.id if c_user.professional_data else None,
        "username":c_user.username,
        "user_id":payload['user_id'],
    })