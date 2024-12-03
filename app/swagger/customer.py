create_customer_dict={
    "summary": "Create a customer",
    "description": "Create a customer.",
    "operationId": "create_customer_controller",
    "tags": [
        "Customer"
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Customer"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Customer created successfully",
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
                                            "example": "Customer account created successfully"
                                        },
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "customer": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 31
                                                        },
                                                        "user_id": {
                                                            "type": "integer",
                                                            "example": 62
                                                        }
                                                    }
                                                },
                                                "user": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 62
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "abcd"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "abcd@gmail.com"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "123"
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "CUSTOMER"
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": "default.jpg"
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
                                                            "example": "Thu, 14 Nov 2024 22:44:53 GMT"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "nullable": True,
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 600036
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": ""
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "abcd"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                },
            },
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

get_customers_dict = {
    "summary":"Get all customers",
    "description":"Get all customers with pagination and sorting options.",
    "operationId": "get_customers_controller",
    "tags": [
        "Customer"
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
                        "description": "Successfully fetched customer details",
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
                                                    "email": {
                                                        "type": "string"
                                                    },
                                                    "blocked": {
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

get_customer_summary_dict = {
    "summary":"Get customer's summary",
    "description":"Get customer's summary.",
    "operationId": "get_customer_summary_controller",
    "tags": [
        "Customer"
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
            "description": "ID of the customer whose summary data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
            "description": "Successful response containing customer service request statistics.",
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
                                                "customer": {
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
                                                        "spending_data": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "day": {
                                                                        "type": "string",
                                                                        "format": "date",
                                                                        "example": "2024-11-14"
                                                                    },
                                                                    "total_spent": {
                                                                        "type": "integer",
                                                                        "example": 2482944
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

get_customer_dict = {
    "summary":"Get a specific customer by ID",
    "description":"Get a specific customer by ID.",
    "operationId": "get_customer_controller",
    "tags": [
        "Customer"
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
            "description": "ID of the customer whose data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
                        "description": "Successful response containing customer details.",
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
                                                "customer": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 16
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Tamanna Halder"
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "customer16"
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": "Voluptatum a enim autem id nam."
                                                        },
                                                        "address": {
                                                            "type": "string",
                                                            "example": "499, Banerjee Path\nMalda 210666"
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
                                                        "email": {
                                                            "type": "string",
                                                            "example": "gollaumang@example.net"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": "11.0168"
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": "76.9558"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "07949393298"
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 254276
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": "Ab De Villiers.jpeg"
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "Customer"
                                                        },
                                                        "recent_reviews": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "description": "List of recent reviews (empty in this response)."
                                                            }
                                                        },
                                                        "recent_service_requests": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "id": {
                                                                        "type": "integer",
                                                                        "example": 16
                                                                    },
                                                                    "customer_id": {
                                                                        "type": "integer",
                                                                        "example": 16
                                                                    },
                                                                    "service_id": {
                                                                        "type": "integer",
                                                                        "example": 16
                                                                    },
                                                                    "service_status": {
                                                                        "type": "string",
                                                                        "example": "REQUESTED"
                                                                    },
                                                                    "start_date": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 30, 2024 12:00 AM"
                                                                    },
                                                                    "total_days": {
                                                                        "type": "integer",
                                                                        "example": 16
                                                                    },
                                                                    "hours_per_day": {
                                                                        "type": "integer",
                                                                        "example": 16
                                                                    },
                                                                    "total_cost": {
                                                                        "type": "integer",
                                                                        "example": 2482944
                                                                    },
                                                                    "date_created": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 01:33 PM"
                                                                    },
                                                                    "date_of_completion": {
                                                                        "type": "string",
                                                                    },
                                                                    "date_updated": {
                                                                        "type": "string",
                                                                        "format": "date-time",
                                                                        "example": "November 14, 2024 01:33 PM"
                                                                    },
                                                                    "remarks": {
                                                                        "type": "string",
                                                                        "example": "Service request 16 remarks"
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

delete_customer_dict = {
    "operationId":"delete_customer_controller",
    "summary": "Delete a specific customer by ID",
    "description": "Delete a specific customer by ID.",
    "tags": [
        "Customer"
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
            "description": "The ID of the customer to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the customer.",
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
                                "example": "Customer deleted successfully"
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

get_customer_profile_dict = {
    "summary":"Get a specific customer's profile by ID",
    "description":"Get a specific customer's profile by ID.",
    "operationId": "get_customer_profile_controller",
    "tags": [
        "Customer"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "id",
            "required": True,
            "description": "ID of the customer whose profile data is being retrieved.",
            "schema": {
                "type": "integer",
                "example": 1
            }
        }
    ],
    "responses" : {
        "200": {
                        "description": "Successful response containing basic customer details.",
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
                                                "customer": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 16
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Tamanna Halder"
                                                        },
                                                        "username": {
                                                            "type": "string",
                                                            "example": "customer16"
                                                        },
                                                        "about": {
                                                            "type": "string",
                                                            "example": "Voluptatum a enim autem id nam."
                                                        },
                                                        "address": {
                                                            "type": "string",
                                                            "example": "499, Banerjee Path\nMalda 210666"
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
                                                        "email": {
                                                            "type": "string",
                                                            "example": "gollaumang@example.net"
                                                        },
                                                        "last_login": {
                                                            "type": "string",
                                                        },
                                                        "latitude": {
                                                            "type": "string",
                                                            "example": "11.0168"
                                                        },
                                                        "longitude": {
                                                            "type": "string",
                                                            "example": "76.9558"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "07949393298"
                                                        },
                                                        "pincode": {
                                                            "type": "integer",
                                                            "example": 254276
                                                        },
                                                        "profile_image": {
                                                            "type": "string",
                                                            "example": "Ab De Villiers.jpeg"
                                                        },
                                                        "role": {
                                                            "type": "string",
                                                            "example": "Customer"
                                                        },
                                                        "recent_reviews": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "object",
                                                                "description": "List of recent reviews (empty in this response)."
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

block_customer_dict = {
                "summary": "Change the status the customer",
                "description": "Change the status the customer.",
                "operationId": "block_customer_controller",
                "tags": [
                    "Customer"
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
                        "description": "The ID of the customer to change status.",
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
                        "description": "Customer's active status changed",
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
                                            "example": "Customer is now blocked"
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

edit_customer_dict = {
    "summary": "Edit a specific customer by ID",
    "description": "Edit a specific customer by ID",
    "operationId": "edit_customer_controller",
    "tags": [
        "Customer"
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
            "description": "The ID of the customer to update.",
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
            "description": "Customer updated successfully",
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
                                "example": "Customer updated successfully"
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
