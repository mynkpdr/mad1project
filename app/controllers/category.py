from datetime import datetime
import pytz
from flask import request, jsonify
from sqlalchemy import asc, desc, func
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from app.models import Category, Service, db
from app.config import PaginationConfig
from app.utils.helpers import validate_fields


# Utility function for dynamic sorting
def get_sorting_field(sort_by, direction):
    if sort_by == "services_count":
        # Count services per category
        sort_field = func.count(Service.id)
    else:
        # Default fields in Category model
        valid_sort_fields = {
            "id": Category.id,
            "name": Category.name,
            "date_created": Category.date_created,
        }
        if sort_by not in valid_sort_fields:
            raise BadRequest(
                f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
            )
        sort_field = valid_sort_fields[sort_by]

    # Ascending or descending based on direction
    return asc(sort_field) if direction == "asc" else desc(sort_field)

# Controller function to get categories
def get_categories_controller():
    # Get and validate query parameters
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", PaginationConfig.DEFAULT_PER_PAGE, type=int)
    sort_by = request.args.get("sort_by", PaginationConfig.DEFAULT_SORT_BY).lower()
    direction = request.args.get("direction", PaginationConfig.DEFAULT_DIRECTION).lower()

    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    # Query categories with count of related services
    query = db.session.query(
        Category,
        func.count(Service.id).label("services_count")
    ).outerjoin(Category.services).group_by(Category.id)

    # Apply dynamic sorting
    query = query.order_by(get_sorting_field(sort_by, direction))

    
    categories_paginated = query.paginate(page=page, per_page=per_page)

    categories_list = []
    for category, services_count in categories_paginated.items:
        services_list = [
            {
                "id": service.id,
                "name": service.name,
                "price": service.price,
                "description": service.description,
            }
            for service in category.services
        ]
        categories_list.append(
            {
                "id": category.id,
                "name": category.name,
                "total_services": services_count,
                "services": services_list,
                "date_created": category.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )

    # Return successful response with pagination metadata
    return (
        jsonify(
            {
                "success": True,
                "data": categories_list,
                "pagination": {
                    "total": categories_paginated.total,
                    "pages": categories_paginated.pages,
                    "prev_num": categories_paginated.prev_num,
                    "next_num": categories_paginated.next_num,
                    "current_page": categories_paginated.page,
                    "per_page": categories_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )


def get_category_controller(category_id):
    # Validate the category ID
    if not category_id or not isinstance(category_id, int):
        raise BadRequest("Invalid category ID provided.")

    category = db.session.query(Category).filter_by(id=category_id).first()

    if not category:
        raise NotFound(f"Service with ID {category_id} not found.")

    services_list = [
        {
            "id": service.id,
            "name": service.name,
            "price": service.price,
            "description": service.description,
            "image": service.image,
            "date_created": service.date_created.strftime("%B %d, %Y %I:%M %p"),
        }
        for service in category.services
    ]

    category_data = {
        "id": category.id,
        "name": category.name,
        "services": services_list,
        "services_count": len(category.services),
        "date_created": category.date_created.strftime("%B %d, %Y %I:%M %p"),
    }

    return jsonify({"success": True, "data": category_data}), 200


def edit_category_controller(category_id):
    category = db.session.query(Category).filter_by(id=category_id).first()
    if category is None:
        raise NotFound(f"Category with ID {category_id} not found.")

    data = request.get_json()

    if not data:
        raise BadRequest("No data provided.")

    name = data.get("name")
    if not name:
        data['name'] = category.name
        name = category.name
    validate_fields(data, [
        ('name', str)
    ])
    category.name = name
    try:
        db.session.commit()
        return jsonify(success=True, message="Category updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating service")


def delete_category_controller(category_id):
    category = db.session.query(Category).filter_by(id=category_id).first()
    if not category:
        raise NotFound(f"Category with ID {category_id} not found.")

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify(success=True, message="Category deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete category with ID {category_id}")


def get_category_services_controller(category_id):
    from app.controllers.service import get_sorting_field

    # Get and validate query parameters
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", PaginationConfig.DEFAULT_PER_PAGE, type=int)
    sort_by = request.args.get(
        "sort_by", PaginationConfig.DEFAULT_SORT_BY
    ).lower()
    direction = request.args.get(
        "direction", PaginationConfig.DEFAULT_DIRECTION
    ).lower()
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    category = Category.query.get(category_id)
    if not category:
        raise NotFound(f"Category with ID {category_id} not found.")

    query = db.session.query(Service).filter_by(category_id=category_id)
    
    query = query.order_by(
        get_sorting_field(sort_by, direction)
    )
    
    
    services_paginated = query.paginate(page=page, per_page=per_page)
    
    services_list = []
    for service in services_paginated.items:
        services_list.append(
            {
                "id": service.id,
                "name": service.name,
                "price": service.price,
                "image": service.image,
                "description": service.description,
                "category": {"id": category.id, "name": category.name},
                "date_created": service.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )
    return (
        jsonify(
            {
                "success": True,
                "data": services_list,
                "pagination": {
                    "total": services_paginated.total,
                    "pages": services_paginated.pages,
                    "prev_num": services_paginated.prev_num,
                    "next_num": services_paginated.next_num,
                    "current_page": services_paginated.page,
                    "per_page": services_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )


def create_category_controller():

    data = request.get_json()
    
    name = data.get("name")

    validate_fields(data, [
        ('name', str),
    ])
    
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category and existing_category.name.lower() == name.lower():
        raise Conflict(f"Category '{name}' already exists.")

    new_category = Category(
        name=name,
        date_created=datetime.now(pytz.timezone("Asia/Kolkata")),  # Set current date and time
    )

    db.session.add(new_category)
    db.session.commit()

    category_data = {column.name: getattr(new_category, column.name) for column in Category.__table__.columns}
    return (
        jsonify(
            {
                "success": True,
                "message": "Category created successfully",
                "data": category_data,
            }
        ),
        201,
    )


def search_category_controller():
    query = request.args.get("q")

    # Get and validate query parameters
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", PaginationConfig.DEFAULT_PER_PAGE, type=int)
    sort_by = request.args.get(
        "sort_by", PaginationConfig.DEFAULT_SORT_BY
    ).lower()
    direction = request.args.get(
        "direction", PaginationConfig.DEFAULT_DIRECTION
    ).lower()
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    category_results = db.session.query(
        Category,
        func.count(Service.id).label("services_count")
    ).outerjoin(Category.services).filter(
            (Service.id.ilike(f"%{query}%"))
            | (Service.name.ilike(f"%{query}%"))
            | (Service.price.ilike(f"%{query}%"))
            | (Category.name.ilike(f"%{query}%"))
            | (Service.description.ilike(f"%{query}%"))
    ).group_by(Category.id)

    category_results = category_results.order_by(get_sorting_field(sort_by, direction))
    
    categories_paginated = category_results.paginate(page=page, per_page=per_page)

    categories_list = []
    for category, services_count in categories_paginated.items:
        services_list = [
            {
                "id": service.id,
                "name": service.name,
                "price": service.price,
                "description": service.description,
            }
            for service in category.services
        ]
        categories_list.append(
            {
                "id": category.id,
                "name": category.name,
                "total_services": services_count,
                "services": services_list,
                "date_created": category.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )
    
    # Return successful response with pagination metadata
    return (
        jsonify(
            {
                "success": True,
                "data": categories_list,
                "pagination": {
                    "total": categories_paginated.total,
                    "pages": categories_paginated.pages,
                    "prev_num": categories_paginated.prev_num,
                    "next_num": categories_paginated.next_num,
                    "current_page": categories_paginated.page,
                    "per_page": categories_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )