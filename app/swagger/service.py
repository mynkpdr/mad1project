create_service_dict={
    "summary": "Create a service",
    "description": "Create a service.",
    "operationId": "create_service_controller",
    "tags": [
        "Service"
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
                    "$ref": "#/components/schemas/Service"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Service created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                            "allOf": [
                                {
                                    "$ref": "#/components/schemas/Service"
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "The date when the service was created"
                                        },
                                    },
                                }
                            ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Service created successfully"
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

get_service_dict={
    "summary": "Get a specific service by ID",
    "description": "Get a specific service with pagination and sorting options.",
    "operationId": "get_service_controller",
    "tags": [
        "Service"
    ],
    "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "ID of the service to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                    {
                        "name": "page",
                        "in": "query",
                        "description": "The page number for pagination",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 1
                        }
                    },
                    {
                        "name": "per_page",
                        "in": "query",
                        "description": "The number of professionals per page",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 20
                        }
                    },
                    {
                        "name": "sort_by",
                        "in": "query",
                        "description": "Sort the professionals by a field (e.g., rating or price)",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": [
                                "rating",
                                "price",
                            ],
                            "default": "rating"
                        }
                    },
                    {
                        "name": "direction",
                        "in": "query",
                        "description": "Direction of the sorting (asc or desc)",
                        "required": False,
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
                        "description": "Successfully fetched service details",
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
                                                    "type": "integer"
                                                },
                                                "name": {
                                                    "type": "string"
                                                },
                                                "price": {
                                                    "type": "integer"
                                                },
                                                "professionals": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "id": {
                                                                "type": "integer"
                                                            },
                                                            "name": {
                                                                "type": "string"
                                                            },
                                                            "image": {
                                                                "type": "string"
                                                            },
                                                            "address": {
                                                                "type": "string"
                                                            },
                                                            "about": {
                                                                "type": "string"
                                                            },
                                                            "price": {
                                                                "type": "integer"
                                                            },
                                                            "total_reviews": {
                                                                "type": "integer"
                                                            },
                                                            "rating": {
                                                                "type": "number",
                                                                "format": "float"
                                                            },
                                                            "total_service_requests_completed": {
                                                                "type": "integer"
                                                            }
                                                        }
                                                    }
                                                },
                                                "image": {
                                                    "type": "string"
                                                },
                                                "description": {
                                                    "type": "string"
                                                },
                                                "category": {
                                                    "type": "object",
                                                    "properties": {
                                                        "id": {
                                                            "type": "integer"
                                                        },
                                                        "name": {
                                                            "type": "string"
                                                        }
                                                    }
                                                },
                                                "date_created": {
                                                    "type": "string",
                                                    "format": "date"
                                                },
                                                "pagination": {
                                                    "type": "object",
                                                    "properties": {
                                                        "total": {
                                                            "type": "integer"
                                                        },
                                                        "pages": {
                                                            "type": "integer"
                                                        },
                                                        "prev_num": {
                                                            "type": "integer",
                                                            "nullable": True
                                                        },
                                                        "next_num": {
                                                            "type": "integer",
                                                            "nullable": True
                                                        },
                                                        "current_page": {
                                                            "type": "integer"
                                                        },
                                                        "per_page": {
                                                            "type": "integer"
                                                        }
                                                    }
                                                },
                                                "sort_by": {
                                                    "type": "string",
                                                    "example": "rating"
                                                },
                                                "direction": {
                                                    "type": "string",
                                                    "example": "desc"
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

get_services_dict = {
    "summary":"Get all services",
    "description":"Get all services with pagination and sorting options.",
    "operationId": "get_services_controller",
    "tags": [
        "Service"
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
                    "price",
                    "category",
                    "description",
                    "date_created",
                    "starting_professional_price"
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
            "description": "Service details fetched successfully",
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
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "integer",
                                            "example": 37
                                        },
                                        "name": {
                                            "type": "string",
                                            "example": "Plumbing"
                                        },
                                        "description": {
                                            "type": "string",
                                            "example": "All quality of Plumbing services available"
                                        },
                                        "price": {
                                            "type": "integer",
                                            "example": 999
                                        },
                                        "image": {
                                            "type": "string",
                                            "example": "default.jpg"
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "example": "November 14, 2024 03:46 PM"
                                        },
                                        "category": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "name": {
                                                    "type": "string",
                                                    "example": "Home Cleaning"
                                                }
                                            }
                                        },
                                        "professionals": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {
                                                        "type": "integer"
                                                    },
                                                    "name": {
                                                        "type": "string"
                                                    }
                                                }
                                            },
                                            "example": []
                                        },
                                        "starting_professional_price": {
                                            "type": "integer",
                                            "nullable": True,
                                            "example": "asd",
                                        },
                                        "total_service_requests": {
                                            "type": "integer",
                                            "example": 0
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

edit_service_dict = {
    "summary": "Edit a specific service by ID",
    "description": "Edit a specific service by ID",
    "operationId": "edit_service_controller",
    "tags": [
        "Service"
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
            "description": "The ID of the service to update.",
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
                    "$ref": "#/components/schemas/Service"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Service updated successfully",
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
                                "example": "Service updated successfully"
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

delete_service_dict = {
    "operationId":"delete_service_controller",
    "summary": "Delete a specific service by ID",
    "description": "Delete a specific service by ID.",
    "tags": [
        "Service"
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
            "description": "The ID of the service to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the service.",
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
                                "example": "Service deleted successfully"
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

get_service_category_dict = {
    "summary": "Get a specific Service's category by ID",
    "description": "Get a specific Service's category",
    "operationId": "get_service_category_controller",
    "tags": [
        "Service"
    ],
    "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "ID of the Service to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
                    "200": {
                        "description": "Successfully fetched service details",
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
                                                    "type": "integer"
                                                },
                                                "name": {
                                                    "type": "string"
                                                },
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

get_service_service_requests_dict = {
    "summary": "Get a specific Service's category by ID",
    "description": "Get a specific Service's category",
    "operationId": "get_service_service_requests_controller",
    "tags": [
        "Service"
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
                        "description": "ID of the Service to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
                    "200": {
                        "description": "Successfully fetched service details",
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
                                            "success": {
                                                "type": "boolean",
                                                "example": True
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
                                                        "customer": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {
                                                                    "type": "integer",
                                                                    "example": 21
                                                                },
                                                                "name": {
                                                                    "type": "string",
                                                                    "example": "Nathaniel Devi"
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
                                                                "service_price": {
                                                                    "type": "integer",
                                                                    "example": 699
                                                                }
                                                            }
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
                                                        "remarks": {
                                                            "type": "string",
                                                            "example": "Service request 21 remarks"
                                                        },
                                                        "review": {
                                                            "type": "integer",
                                                            "nullable": True,
                                                        },
                                                        "service_status": {
                                                            "type": "string",
                                                            "example": "REQUESTED"
                                                        },
                                                        "start_date": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "Thu, 05 Dec 2024 00:00:00 GMT"
                                                        },
                                                        "total_cost": {
                                                            "type": "integer",
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
                                                        "date_created": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "November 14, 2024 01:33 PM"
                                                        },
                                                        "date_of_completion": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "nullable": True,
                                                        },
                                                        "date_updated": {
                                                            "type": "string",
                                                            "format": "date-time",
                                                            "example": "November 14, 2024 01:33 PM"
                                                        }
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

get_nearby_professionals_dict = {
    "summary":"Get professionals by distance",
    "description":"Get professionals by distance.",
    "operationId": "get_nearby_professionals_controller",
    "tags": [
        "Service"
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
                        "description": "ID of the Service to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "distance_km": {
                            "type": "integer",
                            "description": "The distance",
                            "example": 10
                        },
                    },
                },

            }
        }
    },
    "responses": {
        "200": {
            "description": "Professionals fetched successfully",
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
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "user_id": {
                                                "type": "integer",
                                                "example": 21
                                            },
                                            "name": {
                                                "type": "string",
                                                "example": "John Doe"
                                            },
                                            "id": {
                                                "type": "integer",
                                                "example": 1
                                            },
                                            "rating": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 4.5
                                            },
                                            "profile_image": {
                                                "type": "string",
                                                "example": "profile_image.png"
                                            },
                                            "totalreviews": {
                                                "type": "integer",
                                                "example": 25
                                            },
                                            "service_name": {
                                                "type": "string",
                                                "example": "Plumbing"
                                            },
                                            "service_price": {
                                                "type": "integer",
                                                "example": 999
                                            },
                                            "latitude": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 12.9716
                                            },
                                            "longitude": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 77.5946
                                            },
                                            "distance": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 2.5
                                            }
                                        }
                                    }
                                }
                            },
                            "required": [
                                "success",
                                "data"
                            ]
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

get_pincode_professionals_dict = {
    "summary":"Get professionals by pincode",
    "description":"Get professionals by pincode.",
    "operationId": "get_pincode_professionals_controller",
    "tags": [
        "Service"
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
                        "description": "ID of the Service to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "pincode": {
                            "type": "integer",
                            "description": "Pincode",
                            "example": 600036
                        },
                    },
                },

            }
        }
    },
    "responses": {
        "200": {
            "description": "Professionals fetched successfully",
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
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "user_id": {
                                                "type": "integer",
                                                "example": 21
                                            },
                                            "name": {
                                                "type": "string",
                                                "example": "John Doe"
                                            },
                                            "id": {
                                                "type": "integer",
                                                "example": 1
                                            },
                                            "rating": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 4.5
                                            },
                                            "profile_image": {
                                                "type": "string",
                                                "example": "profile_image.png"
                                            },
                                            "totalreviews": {
                                                "type": "integer",
                                                "example": 25
                                            },
                                            "service_name": {
                                                "type": "string",
                                                "example": "Plumbing"
                                            },
                                            "service_price": {
                                                "type": "integer",
                                                "example": 999
                                            },
                                            "latitude": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 12.9716
                                            },
                                            "longitude": {
                                                "type": "number",
                                                "format": "float",
                                                "example": 77.5946
                                            },
                                        }
                                    }
                                }
                            },
                            "required": [
                                "success",
                                "data"
                            ]
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
