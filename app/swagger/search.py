search_dict = {
    "summary":"Search",
    "description":"Search with pagination and sorting options.",
    "operationId": "search_controller",
    "tags": [
        "Search"
    ],
    "parameters": [
        {
            "in": "query",
            "name": "q",
            "required": True,
            "schema": {
                "type": "string"
            },
            "description": "Search term."
        },
        {
            "in": "query",
            "name": "t",
            "required": True,
            "schema": {
                "type": "string",
                "enum" : [
                    "service",
                    "service_request",
                    "professional",
                    "customer",
                    "user",
                    "category",
                    "service",
                    "message",
                ]
            },
        },
        {
            "in": "query",
            "name": "page",
            "schema": {
                "type": "integer",
                "default": 1
            },
            "description": "Page number for pagination."
        },
        {
            "in": "query",
            "name": "per_page",
            "schema": {
                "type": "integer",
                "default": 20
            },
            "description": "Number of results per page."
        },
        {
            "in": "query",
            "name": "sort_by",
            "schema": {
                "type": "string",
                "default": "date_created"
            },
            "description": "Field to sort by (e.g., date_created)."
        },
        {
            "in": "query",
            "name": "direction",
            "schema": {
                "type": "string",
                "enum": [
                    "asc",
                    "desc"
                ],
                "default": "desc"
            },
            "description": "Direction for sorting (ascending or descending)."
        },
        {
            "in": "query",
            "name": "status",
            "schema": {
                "type": "string",
            },
            "description": "Filter by status of the service request."
        },
        {
            "in": "query",
            "name": "start_date",
            "schema": {
                "type": "string",
                "format": "date"
            },
            "description": "Filter by start date (format YYYY-MM-DD) of the service request."
        },
        {
            "in": "query",
            "name": "end_date",
            "schema": {
                "type": "string",
                "format": "date"
            },
            "description": "Filter by end date (format YYYY-MM-DD) of the service request."
        },
    ],
    "responses": {
        "200": {
            "description": "A list of service requests with pagination information.",
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