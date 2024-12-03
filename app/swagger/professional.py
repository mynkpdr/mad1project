create_professional_dict={
    "summary": "Create a professional",
    "description": "Create a professional.",
    "operationId": "create_professional_controller",
    "tags": [
        "Professional"
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Professional"
                },

            }
        }
    },
    "responses": {
        "201": {
                        "description": "Successful response containing professional details.",
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
                                            "example": "Professional account created successfully"
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "professional": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 31
                                                        },
                                                        "active": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "documents": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "experience": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "rating": {
                                                            "type": "number",
                                                            "format": "integer",
                                                            "example": 5
                                                        },
                                                        "service_id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "service_price": {
                                                            "type": "number",
                                                            "format": "integer",
                                                            "example": 999
                                                        },
                                                        "user_id": {
                                                            "type": "integer",
                                                            "example": 65
                                                        }
                                                    }
                                                },
                                                "user": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 65
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Smith John"
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "smith.john"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "smith.john@email.com"
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "address": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "blocked": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "date_created": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "Thu, 14 Nov 2024 23:39:21 GMT"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "9876543210"
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 600036
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "PROFESSIONAL"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
    }
}

get_professionals_dict = {
    "summary":"Get all professionals",
    "description":"Get all professionals with pagination and sorting options.",
    "operationId": "get_professionals_controller",
    "tags": [
        "Professional"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "parameters": [
        {
            "name": "per_page",
            "in": "query",
            "schema": {
                "type": "integer",
                "default": 20
            }
        },
        {
            "name": "page",
            "in": "query",
            "schema": {
                "type": "integer",
                "default": 1
            }
        },
        {
            "name": "sort_by",
            "in": "query",
            "schema": {
                "type": "string",
                "enum": [
                    "id",
                    "name",
                    "email",
                    "service_name",
                    "active",
                    "date_created",
                ],
                "default": "date_created"
            }
        },
        {
            "name": "direction",
            "in": "query",
            "schema": {
                "type": "string",
                "enum": [
                    "asc",
                    "desc"
                ],
                "default": "desc"
            }
        }
    ],
    "responses": {
                    "200": {
                        "description": "Successfully fetched professional details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                            "example": True
                                        },
                                        "data": {
                                            "type": "array",
                                            "items" : {
                                                "type": "object",
                                                "properties": {
                                                    "id": {
                                                        "type": "integer"
                                                    },
                                                    "user_id": {
                                                        "type": "integer"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    },
                                                    "service_name": {
                                                        "type": "string"
                                                    },
                                                    "email": {
                                                        "type": "string"
                                                    },
                                                    "blocked": {
                                                        "type": "boolean"
                                                    },
                                                    "active": {
                                                        "type": "boolean"
                                                    },
                                                    "date_created": {
                                                        "type": "string",
                                                        "format": "date"
                                                    },

                                                }
                                            }
                                        },
                                            "direction": {
                                                "type": "string",
                                                "example": "desc"
                                            },
                                            "pagination": {
                                                "type": "object",
                                                "properties": {
                                                    "current_page": {
                                                        "type": "integer",
                                                        "example": 1
                                                    },
                                                    "next_num": {
                                                        "type": "integer",
                                                        "nullable": True,
                                                    },
                                                    "pages": {
                                                        "type": "integer",
                                                        "example": 1
                                                    },
                                                    "per_page": {
                                                        "type": "integer",
                                                        "example": 20
                                                    },
                                                    "prev_num": {
                                                        "type": "integer",
                                                        "nullable": True,
                                                    },
                                                    "total": {
                                                        "type": "integer",
                                                        "example": 2
                                                    }
                                                }
                                            },
                                            "sort_by": {
                                                "type": "string",
                                                "example": "date_created"
                                            },
                                            "blocked": {
                                                "type": "boolean",
                                                "example": True
                                            }
                                    }
                                }
                            }
                        }
                    },

        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
    }
}

get_professional_summary_dict = {
    "summary":"Get professional's summary",
    "description":"Get professional's summary.",
    "operationId": "get_professional_summary_controller",
    "tags": [
        "Professional"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
            "description": "ID of the professional whose summary data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
            "description": "Successful response containing professional service request statistics.",
            "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                            "example": True
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "professional": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Tamanna Halder"
                                                        },
                                                        "assigned_service_requests_count": {
                                                            "type": "integer",
                                                            "example": 0
                                                        },
                                                        "closed_service_requests_count": {
                                                            "type": "integer",
                                                            "example": 0
                                                        },
                                                        "current_service_requests_count": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "rejected_service_requests_count": {
                                                            "type": "integer",
                                                            "example": 0
                                                        },
                                                        "requested_service_requests_count": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "total_earnings": {
                                                            "type": "integer",
                                                            "example": 9999,
                                                        },
                                                        "total_reviews": {
                                                            "type": "integer",
                                                            "example": 20,
                                                        },
                                                        "rating": {
                                                            "type": "integer",
                                                            "example": 5
                                                        },
                                                        "revenue_data": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "day": {
                                                                        "type": "string",
                                                                        "format": "date",
                                                                        "example": "2024-11-14"
                                                                    },
                                                                    "total_revenue": {
                                                                        "type": "integer",
                                                                        "example": 699
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        "review_counts": {
                                                            "type": "object",
                                                            "properties": {
                                                                "1" : {
                                                                    "type": "integer"
                                                                },
                                                                "2" : {
                                                                    "type": "integer"
                                                                },
                                                                "3" : {
                                                                    "type": "integer"
                                                                },
                                                                "4" : {
                                                                    "type": "integer"
                                                                },
                                                                "5" : {
                                                                    "type": "integer"
                                                                },
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
        },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
        
    }
}

get_professional_dict = {
    "summary":"Get a specific professional by ID",
    "description":"Get a specific professional by ID.",
    "operationId": "get_professional_controller",
    "tags": [
        "Professional"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
            "description": "ID of the professional whose data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
                        "description": "Successful response containing professional details.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                            "example": True
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "professional": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Eta Bose"
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "professional1"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "tanvipillay@example.net"
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": "Quasi molestiae quidem."
                                                        },
                                                        "active": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "address": {
                                                            "type": "string",
                                                            "example": "24/169\nBaria Nagar, Dharmavaram 858443"
                                                        },
                                                        "blocked": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "date_created": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "November 14, 2024 01:33 PM"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": "23.0339"
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": "72.585"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "+915530843760"
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 635815
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": "David Warner.jpg"
                                                        },
                                                        "documents": {
                                                            "type": "string",
                                                            "example": "documents_professional1.pdf"
                                                        },
                                                        "experience": {
                                                            "type": "integer",
                                                            "example": 6
                                                        },
                                                        "rating": {
                                                            "type": "number",
                                                            "format": "integer",
                                                            "example": 5
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "Professional"
                                                        },
                                                        "total_reviews": {
                                                            "type": "integer",
                                                            "example": 4
                                                        },
                                                        "professional_service": {
                                                            "type": "object",
                                                            "properties": {
                                                                "service_id": {
                                                                    "type": "integer",
                                                                    "example": 1
                                                                },
                                                                "service_name": {
                                                                    "type": "string",
                                                                    "example": "Full House Cleaning"
                                                                },
                                                                "service_category": {
                                                                    "type": "string",
                                                                    "example": "Home Cleaning"
                                                                },
                                                                "service_description": {
                                                                    "type": "string",
                                                                    "example": "Deep cleaning of the entire house including kitchen, bathrooms, and all rooms."
                                                                },
                                                                "service_image": {
                                                                    "type": "string",
                                                                    "example": "home.png"
                                                                },
                                                                "service_price": {
                                                                    "type": "number",
                                                                    "format": "integer",
                                                                    "example": 699
                                                                }
                                                            }
                                                        },
                                                        "recent_reviews": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "id": {
                                                                        "type": "integer",
                                                                        "example": 15
                                                                    },
                                                                    "professional_id": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "customer_id": {
                                                                        "type": "integer",
                                                                        "example": 21
                                                                    },
                                                                    "customer_name": {
                                                                        "type": "string",
                                                                        "example": "Nathaniel Devi"
                                                                    },
                                                                    "customer_image": {
                                                                        "type": "string",
                                                                        "example": "Rohit Sharma.png"
                                                                    },
                                                                    "description": {
                                                                        "type": "string",
                                                                        "example": "Excellent service and very professional."
                                                                    },
                                                                    "date_created": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 03:27 PM"
                                                                    },
                                                                    "service_request_id": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "value": {
                                                                        "type": "integer",
                                                                        "example": 5
                                                                    }
                                                                }
                                                            }
                                                        },
                                                        "recent_service_requests": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "id": {
                                                                        "type": "integer",
                                                                        "example": 33
                                                                    },
                                                                    "customer_id": {
                                                                        "type": "integer",
                                                                        "example": 30
                                                                    },
                                                                    "service_id": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "date_created": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 09:35 PM"
                                                                    },
                                                                    "date_of_completion": {
                                                                        "type": "string",
                                                                    },
                                                                    "date_updated": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 09:35 PM"
                                                                    },
                                                                    "start_date": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "December 12, 2024 12:00 AM"
                                                                    },
                                                                    "total_cost": {
                                                                        "type": "number",
                                                                        "format": "integer",
                                                                        "example": 699
                                                                    },
                                                                    "total_days": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "hours_per_day": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "remarks": {
                                                                        "type": "string",
                                                                        "example": "Come early at 10:00 AM"
                                                                    },
                                                                    "review_id": {
                                                                        "type": "integer",
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
        
    }

}

delete_professional_dict = {
    "operationId":"delete_professional_controller",
    "summary": "Delete a specific professional by ID",
    "description": "Delete a specific professional by ID.",
    "tags": [
        "Professional"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
            "description": "The ID of the professional to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the professional.",
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
                                "example": "Professional deleted successfully"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
    },
}

get_professional_profile_dict = {
    "summary":"Get a specific professional's profile by ID",
    "description":"Get a specific professional's profile by ID.",
    "operationId": "get_professional_profile_controller",
    "tags": [
        "Professional"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
            "description": "ID of the professional whose profile data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
                        "description": "Successful response with detailed professional data.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                            "example": True
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "professional": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Eta Bose"
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "professional1"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "tanvipillay@example.net"
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": "Quasi molestiae quidem."
                                                        },
                                                        "active": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "address": {
                                                            "type": "string",
                                                            "example": "24/169\nBaria Nagar, Dharmavaram 858443"
                                                        },
                                                        "blocked": {
                                                            "type": "boolean",
                                                            "example": False
                                                        },
                                                        "date_created": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "November 14, 2024 01:33 PM"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": "23.0339"
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": "72.585"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "+915530843760"
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 635815
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": "David Warner.jpg"
                                                        },
                                                        "documents": {
                                                            "type": "string",
                                                            "example": "documents_professional1.pdf"
                                                        },
                                                        "experience": {
                                                            "type": "integer",
                                                            "example": 6
                                                        },
                                                        "rating": {
                                                            "type": "number",
                                                            "format": "integer",
                                                            "example": 5
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "Professional"
                                                        },
                                                        "total_reviews": {
                                                            "type": "integer",
                                                            "example": 4
                                                        },
                                                        "professional_service": {
                                                            "type": "object",
                                                            "properties": {
                                                                "service_id": {
                                                                    "type": "integer",
                                                                    "example": 1
                                                                },
                                                                "service_name": {
                                                                    "type": "string",
                                                                    "example": "Full House Cleaning"
                                                                },
                                                                "service_category": {
                                                                    "type": "string",
                                                                    "example": "Home Cleaning"
                                                                },
                                                                "service_description": {
                                                                    "type": "string",
                                                                    "example": "Deep cleaning of the entire house including kitchen, bathrooms, and all rooms."
                                                                },
                                                                "service_image": {
                                                                    "type": "string",
                                                                    "example": "home.png"
                                                                },
                                                                "service_price": {
                                                                    "type": "number",
                                                                    "format": "integer",
                                                                    "example": 699
                                                                }
                                                            }
                                                        },
                                                        "recent_reviews": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "id": {
                                                                        "type": "integer",
                                                                        "example": 15
                                                                    },
                                                                    "professional_id": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "professional_name": {
                                                                        "type": "string",
                                                                        "example": "Rayaan Master"
                                                                    },
                                                                    "professional_image": {
                                                                        "type": "string",
                                                                        "example": "Jasprit Bumrah.jpg"
                                                                    },
                                                                    "description": {
                                                                        "type": "string",
                                                                        "example": "Excellent service and very professional."
                                                                    },
                                                                    "date_created": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 03:27 PM"
                                                                    },
                                                                    "service_request_id": {
                                                                        "type": "integer",
                                                                        "example": 1
                                                                    },
                                                                    "value": {
                                                                        "type": "integer",
                                                                        "example": 5
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
        
    }

}

block_professional_dict = {
                "summary": "Change the status the professional",
                "description": "Change the status the professional.",
                "operationId": "block_professional_controller",
                "tags": [
                    "Professional"
                ],
                "security": [
                    {
                        "BearerAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "The ID of the professional to change status.",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "block": {
                                        "type": "boolean",
                                        "example": True
                                    },
                                },
                            },

                        }
                    }
                },
                "responses":{
                    "200": {
                        "description": "Professional's active status changed",
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
                                            "example": "Professional is now blocked"
                                        }
                                    }
                                }
                            }
                        }
                    },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
                    
                    }
}

active_professional_dict = {
                "summary": "Change the status the professional",
                "description": "Change the status the professional.",
                "operationId": "active_professional_controller",
                "tags": [
                    "Professional"
                ],
                "security": [
                    {
                        "BearerAuth": []
                    }
                ],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "The ID of the professional to change status.",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "active": {
                                        "type": "boolean",
                                        "example": True
                                    },
                                },
                            },

                        }
                    }
                },
                "responses":{
                    "200": {
                        "description": "Professional's active status changed",
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
                                            "example": "Professional is now blocked"
                                        }
                                    }
                                }
                            }
                        }
                    },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
                    
                    }
}

edit_professional_dict = {
    "summary": "Edit a specific professional by ID",
    "description": "Edit a specific professional by ID",
    "operationId": "edit_professional_controller",
    "tags": [
        "Professional"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "description": "The ID of the professional to update.",
            "required": True,
            "schema": {
                "type": "integer"
            }
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "email": {
                        "type": "string",
                    },
                    "username": {
                        "type": "string",
                    },
                    "phone": {
                        "type": "string",
                    },
                    "address": {
                        "type": "string",
                    },
                    "pincode": {
                        "type": "integer",
                    },
                    "about": {
                        "type": "string",
                    },
                    "latitude": {
                        "type": "string",
                    },
                    "longitude": {
                        "type": "string",
                    },
                    "profile_image": {
                        "type": "string",
                    },
                    "new_password": {
                        "type": "string",
                    },
                    "current_password": {
                        "type": "string",
                    }
                },
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Professional updated successfully",
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
                                "example": "Professional updated successfully"
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/BadRequestError"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/UnauthorizedError"
                    }
                }
            }
        },
        "403": {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ForbiddenError"
                    }
                }
            }
        },
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/NotFoundError"
                    }
                }
            }
        },
        "409": {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/ConflictError"
                    }
                }
            }
        },
        "500": {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/InternalServerError"
                    }
                }
            }
        }
    }
}
