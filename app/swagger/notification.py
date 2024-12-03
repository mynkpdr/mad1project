create_notification_dict={
    "summary": "Create a notification",
    "description": "Create a notification.",
    "operationId": "create_notification_controller",
    "tags": [
        "Notification"
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
                    "$ref": "#/components/schemas/Notification"
                },

            }
        }
    },
    "responses": {
        "201": {
            "description": "Notification created successfully",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                            "allOf": [
                                {
                                    "$ref": "#/components/schemas/Notification"
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "integer",
                                            "example": 1,
                                        },
                                        "is_read": {
                                            "type": "boolean",
                                            "example": False,
                                        },
                                        "date_created": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "The date when the notification was created"
                                        },
                                    },
                                }
                            ]
                            },
                            "message": {
                                "type": "string",
                                "example": "Notification created successfully"
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

get_notifications_dict = {
    "summary":"Get all notifications",
    "description":"Get all notifications with pagination and sorting options.",
    "operationId": "get_notifications_controller",
    "tags": [
        "Notification"
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
                    "link",
                    "message",
                    "user_id",
                    "is_read",
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
                        "description": "Successfully fetched notification details",
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
                                                        "example": 157
                                                    },
                                                    "date_created": {
                                                        "type": "string",
                                                        "format": "date-time",
                                                        "example": "Thu, 14 Nov 2024 21:35:23 GMT"
                                                    },
                                                    "link": {
                                                        "type": "string",
                                                        "example": "/admin/service_request/33"
                                                    },
                                                    "message": {
                                                        "type": "string",
                                                        "example": "New Service Request"
                                                    },
                                                    "user_id": {
                                                        "type": "integer",
                                                        "example": 1
                                                    },
                                                    "is_read": {
                                                        "type": "boolean",
                                                        "example": False
                                                    }
                                                }
                                            }
                                        },
                                        "pagination": {
                                            "type": "object",
                                            "properties": {
                                                "total": {
                                                    "type": "integer",
                                                    "example": 93
                                                },
                                                "pages": {
                                                    "type": "integer",
                                                    "example": 5
                                                },
                                                "prev_num": {
                                                    "type": "integer",
                                                    "nullable": True,
                                                },
                                                "next_num": {
                                                    "type": "integer",
                                                    "nullable": True,
                                                    "example": 2
                                                },
                                                "current_page": {
                                                    "type": "integer",
                                                    "example": 1
                                                },
                                                "per_page": {
                                                    "type": "integer",
                                                    "example": 20
                                                }
                                            }
                                        },
                                        "sort_by": {
                                            "type": "string",
                                            "example": "date_created"
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

get_notification_dict={
    "summary": "Get a specific notification by ID",
    "description": "Get a specific notification by ID.",
    "operationId": "get_notification_controller",
    "tags": [
        "Notification"
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
                        "description": "ID of the notification to fetch",
                        "required": True,
                        "schema": {
                            "type": "integer"
                        }
                    },
                ],
    "responses": {
        "200": {
            "description": "Notification details fetched successfully",
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
                                        "link": {
                                            "type": "string",
                                            "example": "/service_request/18"
                                        },
                                        "is_read": {
                                            "type": "boolean",
                                            "example": False
                                        },
                                        "message": {
                                            "type": "string",
                                            "example": "New user"
                                        },
                                        "user_id": {
                                            "type": "integer",
                                            "example": 1
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

edit_notification_dict = {
    "summary": "Edit a specific notification by ID",
    "description": "Edit a specific notification by ID",
    "operationId": "edit_notification_controller",
    "tags": [
        "Notification"
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
            "description": "The ID of the notification to update.",
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
                    "$ref": "#/components/schemas/Notification"
                }
            }
        }
    },
    "responses": {
        "200": {
            "description": "Notification updated successfully",
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
                                "example": "Notification updated successfully"
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

delete_notification_dict = {
    "operationId":"delete_notification_controller",
    "summary": "Delete a specific notification by ID",
    "description": "Delete a specific notification by ID.",
    "tags": [
        "Notification"
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
            "description": "The ID of the notification to delete.",
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Successful deletion of the notification.",
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
                                "example": "Notification deleted successfully"
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

read_notification_dict = {
                "summary": "Mark notification(s) as read",
                "description": "Mark notification(s) as read.",
                "operationId": "read_notification_controller",
                "tags": [
                    "Notification"
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
                        "description": "The ID of the notification to mark as read. Use `0` to mark all unread notifications as read.",
                        "required": True,
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "responses":{
                    "200": {
                        "description": "Notification(s) marked as read successfully.",
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
                                            "example": "Notification successfully read"
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