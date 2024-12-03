create_service_request_dict={
    "summary": "Create a service request",
    "description": "Create a service request.",
    "operationId": "create_service_request_controller",
    "tags": [
        "ServiceRequest"
    ],
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/ServiceRequest"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Service Request created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                            "allOf": [
                                {
                                    "$ref": "#/components/schemas/ServiceRequest"
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "total_cost": {
                                            "type": "integer",
                                            "example": 12499,
                                        },
                                        "service_status": {
                                            "type": "string",
                                            "example": "REQUESTED",
                                        },
                                        "review_id": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "The date when the service request was created"
                                        },
                                        "date_updated": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "The date when the service request was updated"
                                        },
                                        "date_of_completion": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "The date when the service request was completed",
                                        },
                                    },
                                }
                            ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Service Request created successfully"
                            },
                            "success": {
                                "type": "boolean",
                                "example": True
                            }
                        },
                        "required": [
                            "data",
                            "message",
                            "success"
                        ],
                    },
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

get_service_requests_dict={
    "summary":"Get all service requests",
    "description":"Get all service requests with pagination and sorting options.",
    "operationId": "get_service_requests_controller",
    "tags": [
        "ServiceRequest"
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
                    "start_date",
                    "total_days",
                    "hours_per_day",
                    "total_cost",
                    "service_status",
                    "service_name",
                    "customer_name",
                    "professional_name",
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
        },
        {
            "name": "status",
            "in": "query",
            "required": False,
            "schema": {
                "type": "string",
                "enum": [
                    "REQUESTED",
                    "ASSIGNED",
                    "CLOSED",
                    "REJECTED"
                ],
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Service Requests details fetched successfully",
            "content": {
                "application/json": {
                    "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {
                                            "type": "boolean",
                                        },
                                        "data": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {
                                                        "type": "integer",
                                                        "example": 21
                                                    },
                                                    "service": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer",
                                                                "example": 1
                                                            },
                                                            "name": {
                                                                "type": "string",
                                                                "example": "Full House Cleaning"
                                                            },
                                                            "price": {
                                                                "type": "integer",
                                                                "example": 2499
                                                            }
                                                        }
                                                    },
                                                    "customer": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer",
                                                                "example": 1
                                                            },
                                                            "name": {
                                                                "type": "string",
                                                                "example": "John Doe"
                                                            }
                                                        }
                                                    },
                                                    "professional": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer",
                                                                "example": 2
                                                            },
                                                            "name": {
                                                                "type": "string",
                                                                "example": "Eta Bose"
                                                            },
                                                            "service_price": {
                                                                "type": "integer",
                                                                "example": 699
                                                            }
                                                        }
                                                    },
                                                    "review": {
                                                        "type": "integer",
                                                    },
                                                    "start_date": {
                                                        "type": "string",
                                                        "format": "date-time",
                                                        "example": "November 14, 2024 01:33 PM"
                                                    },
                                                    "total_days": {
                                                        "type": "integer",
                                                        "example": 1
                                                    },
                                                    "hours_per_day": {
                                                        "type": "integer",
                                                        "example": 8
                                                    },
                                                    "total_cost": {
                                                        "type": "integer",
                                                        "example": 699
                                                    },
                                                    "date_of_completion": {
                                                        "type": "string",
                                                        "format": "date-time",
                                                        "example": "November 14, 2024 03:00 PM"
                                                    },
                                                    "service_status": {
                                                        "type": "string",
                                                        "example": "REQUESTED"
                                                    },
                                                    "remarks": {
                                                        "type": "string",
                                                        "example": "Service request 21 remarks"
                                                    },
                                                    "date_created": {
                                                        "type": "string",
                                                        "format": "date-time",
                                                        "example": "November 14, 2024 01:33 PM"
                                                    },
                                                    "date_updated": {
                                                        "type": "string",
                                                        "format": "date-time",
                                                        "example": "November 14, 2024 02:00 PM"
                                                    }
                                                }
                                            }
                                        },
                                        "pagination": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                    "type": "integer",
                                                    "example": 100
                                                },
                                                "pages": {
                                                    "type": "integer",
                                                    "example": 10
                                                },
                                                "prev_num": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "next_num": {
                                                    "type": "integer",
                                                    "example": 3
                                                },
                                                "current_page": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "per_page": {
                                                    "type": "integer",
                                                    "example": 10
                                                }
                                            }
                                        },
                                        "sort_by": {
                                            "type": "string",
                                            "example": "date_created"
                                        },
                                        "status": {
                                            "type": "string",
                                            "example": "REQUESTED"
                                        },
                                        "direction": {
                                            "type": "string",
                                            "example": "desc"
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

edit_service_request_dict = {
    "summary": "Edit a specific service request by ID",
    "description": "Edit a specific service request by ID",
    "operationId": "edit_service_request_controller",
    "tags": [
        "ServiceRequest"
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
            "description": "The ID of the service request to update.",
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
                    "$ref": "#/components/schemas/ServiceRequest"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Service Request updated successfully",
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
                                "example": "Service Request updated successfully"
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

delete_service_request_dict = {
    "operationId":"delete_service_request_controller",
    "summary": "Delete a specific service request by ID",
    "description": "Delete a specific service request by ID.",
    "tags": [
        "ServiceRequest"
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
            "description": "The ID of the service request to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the service request.",
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
                                "example": "Service Request deleted successfully"
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

get_service_request_dict={
    "summary": "Get a specific service request by ID",
    "description": "Get a specific service request",
    "operationId": "get_service_request_controller",
    "tags": [
        "ServiceRequest"
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
                        "description": "ID of the service request to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
                    "200": {
                        "description": "Successfully fetched service request details",
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
                                                "id": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "service": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Full House Cleaning"
                                                        },
                                                        "price": {
                                                            "type": "integer",
                                                            "example": 2499
                                                        },
                                                        "image": {
                                                            "type": "string",
                                                            "example": "home.png"
                                                        },
                                                        "description": {
                                                            "type": "string",
                                                            "example": "Deep cleaning of the entire house including kitchen, bathrooms, and all rooms."
                                                        },
                                                        "category_name": {
                                                            "type": "string",
                                                            "example": "Home Cleaning"
                                                        },
                                                        "category_id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        }
                                                    }
                                                },
                                                "customer": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "example": "Rayaan Master"
                                                        },
                                                        "image": {
                                                            "type": "string",
                                                            "example": "Jasprit Bumrah.jpg"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "06238097358"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "avimangat@example.com"
                                                        }
                                                    }
                                                },
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
                                                        "image": {
                                                            "type": "string",
                                                            "example": "David Warner.jpg"
                                                        },
                                                        "phone": {
                                                            "type": "string",
                                                            "example": "+915530843760"
                                                        },
                                                        "email": {
                                                            "type": "string",
                                                            "example": "tanvipillay@example.net"
                                                        },
                                                        "service_price": {
                                                            "type": "integer",
                                                            "example": 699
                                                        }
                                                    }
                                                },
                                                "review": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer",
                                                            "example": 1
                                                        },
                                                        "value": {
                                                            "type": "integer",
                                                            "example": 5
                                                        },
                                                        "date_created": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "November 14, 2024 01:33 PM"
                                                        },
                                                        "description": {
                                                            "type": "string",
                                                            "example": "Quod provident quaerat animi ducimus veniam. Laborum voluptates optio repellat et corrupti quo."
                                                        }
                                                    }
                                                },
                                                "start_date": {
                                                    "type": "string",
                                                    "format": "date",
                                                    "example": "November 15, 2024"
                                                },
                                                "total_days": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "hours_per_day": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "total_cost": {
                                                    "type": "integer",
                                                    "example": 699
                                                },
                                                "date_of_completion": {
                                                    "type": "string",
                                                    "format": "date-time",
                                                    "example": "November 14, 2024 01:33 PM"
                                                },
                                                "service_status": {
                                                    "type": "string",
                                                    "example": "CLOSED"
                                                },
                                                "remarks": {
                                                    "type": "string",
                                                    "example": "Service request 1 remarks"
                                                },
                                                "date_created": {
                                                    "type": "string",
                                                    "format": "date-time",
                                                    "example": "November 14, 2024 01:33 PM"
                                                },
                                                "date_updated": {
                                                    "type": "string",
                                                    "format": "date-time",
                                                    "example": "November 14, 2024 01:33 PM"
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
