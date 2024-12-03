from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

swagger_config = {
    "openapi": "3.0.0",
    "info": {
        "title": "A to Z Household Services API",
        "version": "1.0.0",
        "contact": {
            "name": "Mayank Kumar Poddar",
            "url": "https://www.github.com/mynkpdr",
        },
        "description": "API documentation using OpenAPI 3.0 for A to Z Household Services website.",
        "termsOfService": "../terms",
        "x-homepage": "http://www.google.com",
    },
"specs": [
    {
        "endpoint": "swagger",
        "route": "/swagger/swagger.json",
    }
],
"specs_route": "/swagger/",
    "components": {
        "securitySchemes": {
        "BearerAuth": {
            "description": "Enter JWT token to authorize the requests...",
            "scheme": "bearer",
            "type": "http"
        }
        },
        "schemas": {
        "BadRequestError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Bad Request"
                        },
                        "message": {
                            "type": "string",
                            "example": "Invalid request"
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "UnauthorizedError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Unauthorized"
                        },
                        "message": {
                            "type": "string",
                            "example": "You are not authorized."
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "ForbiddenError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Forbidden"
                        },
                        "message": {
                            "type": "string",
                            "example": "You do not have access to this resource."
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "NotFoundError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Not Found"
                        },
                        "message": {
                            "type": "string",
                            "example": "The requested resource could not be found."
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "ConflictError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Conflict"
                        },
                        "message": {
                            "type": "string",
                            "example": "The data you are trying to submit conflicts with an existing resource."
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "InternalServerError": {
                    "type": "object",
                    "properties": {
                        "success": {
                            "type": "boolean",
                            "example": False
                        },
                        "error": {
                            "type": "string",
                            "example": "Internal Server Error"
                        },
                        "message": {
                            "type": "string",
                            "example": "An error occured."
                        }
                    },
                    "required": [
                        "success"
                        "error"
                        "message"
                    ]
                },
        "Review": {
            "type": "object",
            "properties": {
                "professional_id": {
                    "type": "integer",
                    "description": "The ID of the professional being reviewed",
                    "example": 1
                },
                "customer_id": {
                    "type": "integer",
                    "description": "The ID of the customer submitting the review",
                    "example": 1
                },
                "service_request_id": {
                    "type": "integer",
                    "description": "The ID of the service request being reviewed",
                    "example": 1
                },
                "description": {
                    "type": "string",
                    "description": "The content of the review provided by the customer",
                    "example": "Excellent service and very professional."
                },
                "value": {
                    "type": "integer",
                    "description": "The value or rating given by the customer (e.g., score or amount)",
                    "example": 5
                }
            },
            "required": [
                "professional_id",
                "customer_id",
                "service_request_id",
                "value"
            ]
        },
        "Category" : {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "example": "Carpentry",
                    "description": "The name of the category"
                },
            },
            "required": [
                "name",
            ]
        },
        "Contact": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "example": "John Smith",
                    "description": "The name of the contact person"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.smith@email.com",
                    "description": "The email address of the contact person"
                },
                "phone": {
                    "type": "string",
                    "example": "9876543210",
                    "description": "The phone number of the contact person"
                },
                "message": {
                    "type": "string",
                    "example": "Hi, I have query regarding the services available.",
                    "description": "The message or inquiry sent by the contact person"
                }
            },
            "required": [
                "name",
                "email",
                "phone",
                "message"
            ]
        },
        "Customer": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "example": "John Smith",
                    "description": "The user's full name"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.smith@email.com",
                    "description": "The user's email address"
                },
                "username": {
                    "type": "string",
                    "example": "john.smith",
                    "description": "The user's chosen username"
                },
                "phone": {
                    "type": "string",
                    "example": "9876543210",
                    "description": "The user's phone number"
                },
                "address": {
                    "type": "string",
                    "example": "IITM BS Degree Office, 3rd Floor, ICSR Building, IIT Madras, Chennai",
                    "description": "The user's address",
                    "default": ""
                },
                "pincode": {
                    "type": "integer",
                    "example": 600036,
                    "description": "The user's postal code"
                },
                "about": {
                    "type": "string",
                    "example": "John Smith is a passionate software engineer with over 5 years of experience in developing innovative web applications.",
                    "description": "A brief description about the user"
                },
                "latitude": {
                    "type": "string",
                    "example": "12.9914269",
                    "description": "The user's latitude",
                    "default": ""
                },
                "longitude": {
                    "type": "string",
                    "example": "80.2337286",
                    "description": "The user's longitude",
                    "default": ""
                },
                "profile_image": {
                    "type": "string",
                    "example": "default.jpg",
                    "description": "The user's profile image filename",
                    "default": "default.jpg"
                },
                "password": {
                    "type": "string",
                    "example": "12345678",
                    "format": "password",
                    "description": "The user's password"
                }
            },
            "required": [
                "name",
                "email",
                "username",
                "phone",
                "pincode",
                "password"
            ]
        },
        "Notification": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "example": "New user",
                    "description": "The notification message"
                },
                "link": {
                    "type": "string",
                    "example": "/service_request/18",
                    "description": "The link associated with the notification"
                },
                "user_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "The ID of the user receiving the notification"
                }
            },
            "required": [
                "message",
                "link",
                "user_id",
            ]
        },
        "Professional": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "example": "John Smith",
                    "description": "The user's full name"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.smith@email.com",
                    "description": "The user's email address"
                },
                "username": {
                    "type": "string",
                    "example": "john.smith",
                    "description": "The user's chosen username"
                },
                "phone": {
                    "type": "string",
                    "example": "9876543210",
                    "description": "The user's phone number"
                },
                "address": {
                    "type": "string",
                    "example": "IITM BS Degree Office, 3rd Floor, ICSR Building, IIT Madras, Chennai",
                    "description": "The user's address",
                    "default": ""
                },
                "pincode": {
                    "type": "integer",
                    "example": 600036,
                    "description": "The user's postal code"
                },
                "about": {
                    "type": "string",
                    "example": "John Smith is a passionate software engineer with over 5 years of experience in developing innovative web applications.",
                    "description": "A brief description about the user"
                },
                "latitude": {
                    "type": "string",
                    "example": "12.9914269",
                    "description": "The user's latitude",
                    "default": ""
                },
                "longitude": {
                    "type": "string",
                    "example": "80.2337286",
                    "description": "The user's longitude",
                    "default": ""
                },
                "service_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "The ID of the service offered by the professional"
                },
                "service_price": {
                    "type": "integer",
                    "example": 999,
                    "description": "The price of the service offered by the professional"
                },
                "experience": {
                    "type": "integer",
                    "example": 1,
                    "description": "The professional's years of experience (optional)",
                },
                "documents": {
                    "type": "string",
                    "example": "document.pdf",
                    "description": "Links or filenames of documents uploaded by the professional (optional)",
                },
                "profile_image": {
                    "type": "string",
                    "example": "default.jpg",
                    "description": "The filename of the professional's profile image",
                    "default": "default.jpg"
                },
                "password": {
                    "type": "string",
                    "format": "password",
                    "example": "12345678",
                    "description": "The professional's password"
                }
            },
            "required": [
                "name",
                "email",
                "username",
                "phone",
                "password",
                "pincode",
                "service_id",
                "service_price",
            ]
        },
        "ServiceRequest": {
            "type": "object",
            "properties": {
                "service_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "The ID of the service requested"
                },
                "customer_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "The ID of the customer making the request"
                },
                "professional_id": {
                    "type": "integer",
                    "example": 1,
                    "description": "The ID of the professional assigned to the request"
                },
                "total_days": {
                    "type": "integer",
                    "example": 1,
                    "description": "The total number of days for the service request"
                },
                "remarks": {
                    "type": "string",
                    "example": "Come early at 10:00 AM",
                    "description": "Additional remarks or comments regarding the service request"
                },
                "hours_per_day": {
                    "type": "integer",
                    "example": 1,
                    "description": "The number of hours the professional will work each day"
                },
                "start_date": {
                    "type": "string",
                    "format": "date",
                    "example": "2024-12-12",
                    "description": "The start date for the service request"
                }
            },
            "required": [
                "service_id",
                "customer_id",
                "professional_id",
                "total_days",
                "hours_per_day",
                "start_date",
                "remarks",
            ]
        },
        "Service": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the service",
                    "example": "Plumbing"
                },
                "price": {
                    "type": "integer",
                    "description": "The price of the service",
                    "example": 999,
                },
                "description": {
                    "type": "string",
                    "description": "A detailed description of the service",
                    "example": "All quality of Plumbing services available"
                },
                "category_id": {
                    "type": "integer",
                    "description": "The ID of the category the service belongs to",
                    "example": 1,
                },
                "image": {
                    "type": "string",
                    "description": "The image associated with the service",
                    "default": "default.jpg",
                    "example": "default.jpg"
                }
            },
            "required": [
                "name",
                "price",
                "category_id",
                "description"
            ]
        },
        },
    },
    "security": [
        {"BearerAuth": []},
    ]
}


class BaseConfig:
    """Base configuration with common settings for all environments."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    
    # General configurations
    MAX_FILE_SIZE = 1 * 1024 * 1024  # Limit file upload size to 1 MB
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Limit payload size to 10 MB
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)  # Default to False
    
    PROFESSIONAL_DOCUMENT_UPLOAD_FOLDER = os.getenv('PROFESSIONAL_DOCUMENT_UPLOAD_FOLDER', 'uploads/professional_docs')
    PROFILE_IMAGE_UPLOAD_FOLDER = os.getenv('PROFILE_IMAGE_UPLOAD_FOLDER', 'uploads/profile_images')
    SERVICE_IMAGE_UPLOAD_FOLDER = os.getenv('SERVICE_IMAGE_UPLOAD_FOLDER', 'uploads/service_images')

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

    SWAGGER = swagger_config
    API_URL = os.getenv('BASE_API_URL', 'http://127.0.0.1:5000')


class DevelopmentConfig(BaseConfig):
    """Development-specific configuration."""
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    """Production configuration settings."""
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    #OTHER DETAILS


class PaginationConfig:
    """Pagination configuration settings."""
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    DEFAULT_SORT_BY = 'date_created'
    DEFAULT_DIRECTION = 'desc'

config_options = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
