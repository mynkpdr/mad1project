create_category_dict={
    "summary": "Create a category",
    "description": "Create a category.",
    "operationId": "create_category_controller",
    "tags": [
        "Category"
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
                    "$ref": "#/components/schemas/Category"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Category created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                            "allOf": [
                                {
                                    "$ref": "#/components/schemas/Category"
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
                                            "description": "The date when the category was created"
                                        },
                                    },
                                }
                            ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Category created successfully"
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

get_category_dict={
    "summary": "Get a specific category by ID",
    "description": "Get a specific category by ID.",
    "operationId": "get_category_controller",
    "tags": [
        "Category"
    ],
    "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "ID of the category to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
        "200": {
            "description": "Category details fetched successfully",
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
                                            "example": 1
                                        },
                                        "name": {
                                            "type": "string",
                                            "example": "Carpentry"
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "example": "December 12, 2024 03:46 PM"
                                        },
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

get_categories_dict = {
    "summary":"Get all categories",
    "description":"Get all categories with pagination and sorting options.",
    "operationId": "get_categories_controller",
    "tags": [
        "Category"
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
                        "description": "Successfully fetched category details",
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
                                                "services_count": {
                                                    "type": "integer"
                                                },
                                                "services": {
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
                                                            "price": {
                                                                "type": "integer"
                                                            },
                                                            "description": {
                                                                "type"  : "string"
                                                            },
                                                            "date_created": {
                                                                "type": "string",
                                                                "format": "date"
                                                            },
                                                        }
                                                    }
                                                },
                                                "date_created": {
                                                    "type": "string",
                                                    "format": "date"
                                                },
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

edit_category_dict = {
    "summary": "Edit a specific category by ID",
    "description": "Edit a specific category by ID",
    "operationId": "edit_category_controller",
    "tags": [
        "Category"
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
            "description": "The ID of the category to update.",
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
                    "$ref": "#/components/schemas/Category"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Category updated successfully",
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
                                "example": "Category updated successfully"
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

delete_category_dict = {
    "operationId":"delete_category_controller",
    "summary": "Delete a specific category by ID",
    "description": "Delete a specific category by ID.",
    "tags": [
        "Category"
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
            "description": "The ID of the category to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the category.",
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
                                "example": "Category deleted successfully"
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

get_category_services_dict = {
    "summary": "Get a specific Category's services by ID",
    "description": "Get a specific Category's services",
    "operationId": "get_category_services_controller",
    "tags": [
        "Category"
    ],
    "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "description": "ID of the Category to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
                    "200": {
                        "description": "Successfully fetched category details",
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
                                                "example": 15
                                            },
                                            "name": {
                                                "type": "string",
                                                "example": "Fence Painting"
                                            },
                                            "description": {
                                                "type": "string",
                                                "example": "Painting of wooden or metal fences."
                                            },
                                            "price": {
                                                "type": "integer",
                                                "example": 1999
                                            },
                                            "image": {
                                                "type": "string",
                                                "example": "painter.png"
                                            },
                                            "date_created": {
                                                "type": "string",
                                                "format": "date-time",
                                                "example": "November 14, 2024 01:33 PM"
                                            },
                                            "category": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {
                                                        "type": "integer",
                                                        "example": 5
                                                    },
                                                    "name": {
                                                        "type": "string",
                                                        "example": "Painting"
                                                    }
                                                }
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
                                            "example": 3
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

