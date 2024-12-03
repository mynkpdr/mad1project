create_review_dict={
    "summary": "Create a review",
    "description": "Create a review",
    "operationId": "create_review_controller",
    "tags": [
        "Review"
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
                    "$ref": "#/components/schemas/Review"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Review created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                            "allOf": [
                                {
                                    "$ref": "#/components/schemas/Review"
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
                                            "description": "The date when the review was created"
                                        },
                                    },
                                }
                            ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Review created successfully"
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


get_reviews_dict = {
    "summary":"Get all reviews",
    "description":"Get all reviews with pagination and sorting options.",
    "operationId": "get_reviews_controller",
    "tags": [
        "Review"
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
                    "customer_name",
                    "professional_name",
                    "value",
                    "description",
                    "date_created"
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
            "description": "A list of reviews with pagination",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "integer"
                                        },
                                        "customer": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer"
                                                },
                                                "name": {
                                                    "type": "string"
                                                },
                                                "profile_image": {
                                                    "type": "string"
                                                },
                                                "user_id": {
                                                    "type": "integer"
                                                }
                                            }
                                        },
                                        "professional": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer"
                                                },
                                                "name": {
                                                    "type": "string"
                                                },
                                                "profile_image": {
                                                    "type": "string"
                                                },
                                                "user_id": {
                                                    "type": "integer"
                                                }
                                            }
                                        },
                                        "service_request": {
                                            "type": "object",
                                            "properties": {
                                                "id": {
                                                    "type": "integer"
                                                }
                                            }
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "example": "November 13, 2024 11:54 PM"
                                        },
                                        "description": {
                                            "type": "string",
                                            "nullable": True
                                        },
                                        "value": {
                                            "type": "integer"
                                        }
                                    }
                                }
                            },
                            "pagination": {
                                "type": "object",
                                "properties": {
                                    "current_page": {
                                        "type": "integer"
                                    },
                                    "next_num": {
                                        "type": "integer",
                                        "nullable": True
                                    },
                                    "pages": {
                                        "type": "integer"
                                    },
                                    "per_page": {
                                        "type": "integer"
                                    },
                                    "prev_num": {
                                        "type": "integer",
                                        "nullable": True
                                    },
                                    "total": {
                                        "type": "integer"
                                    }
                                }
                            },
                            "direction": {
                                "type": "string",
                                "example": "desc"
                            },
                            "sort_by": {
                                "type": "string",
                                "example": "date_created"
                            },
                            "success": {
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


delete_review_dict = {
    "operationId": "delete_review_controller",
    "summary": "Delete a specific review by ID",
    "description": "Delete a specific review by ID.",
    "tags": [
        "Review"
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
            "description": "The ID of the review to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the review.",
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
                                "example": "Review deleted successfully"
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