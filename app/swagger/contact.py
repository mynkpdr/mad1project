create_contact_dict={
    "summary": "Create a contact",
    "description": "Create a contact.",
    "operationId": "create_contact_controller",
    "tags": [
        "Contact"
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/Contact"
                }
            }
        }
    },
    "responses": {
        "201": {
            "description": "Contact created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "allOf": [
                                    {
                                        "$ref": "#/components/schemas/Contact"
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "date_created": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "The date when the contact was created"
                                            },
                                            "id": {
                                                "type": "integer",
                                                "example": 1
                                            }
                                        }
                                    }
                                ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Contact created successfully"
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


get_contact_dict={
    "summary": "Get a specific contact by ID",
    "description": "Get a specific contact.",
    "operationId": "get_contact_controller",
    "tags": [
        "Contact"
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
            "description": "ID of the contact to fetch",
            "required": True,
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successfully fetched contact details",
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
                                "allOf": [
                                    {
                                        "$ref": "#/components/schemas/Contact"
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "date_created": {
                                                "type": "string",
                                                "format": "date-time",
                                                "description": "The date when the contact was created"
                                            },
                                            "id": {
                                                "type": "integer",
                                                "example": 1
                                            }
                                        }
                                    }
                                ]
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


get_contacts_dict = {
    "summary": "Get all contacts",
    "description": "Get all contacts with pagination and sorting options.",
    "operationId": "get_contacts_controller",
    "tags": [
        "Contact"
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
                    "phone",
                    "message",
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
            "description": "Contact details fetched successfully",
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
                                        "email": {
                                            "type": "string",
                                            "example": "All quality of Plumbing contacts available"
                                        },
                                        "phone": {
                                            "type": "integer",
                                            "example": 999
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "default.jpg"
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "example": "November 14, 2024 03:46 PM"
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


delete_contact_dict = {
    "operationId": "delete_contact_controller",
    "summary": "Delete a specific contact by ID",
    "description": "Delete a specific contact by ID.",
    "tags": [
        "Contact"
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
            "description": "The ID of the contact to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the contact.",
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
                                "example": "Contact deleted successfully"
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