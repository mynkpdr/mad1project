from flask import request, jsonify
from sqlalchemy import asc, desc
from werkzeug.exceptions import BadRequest

from app.models import User
from app.config import PaginationConfig


def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": User.id,
        "name": User.name,
        "email": User.email,
        "role": User.role.name,
        "date_created": User.date_created,
    }
    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)

def get_users_controller():
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
    user = User.query.order_by(get_sorting_field(sort_by, direction))

    
    users_paginated = user.paginate(page=page, per_page=per_page)
    
    users_list = []
    for user in users_paginated.items:
        if user.customer_data:
            users_list.append(
                {
                    "id": user.id,
                    "customer_id": user.customer_data.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.name,
                    "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
                }
            )
        elif user.professional_data:
            users_list.append(
            {
                    "id": user.id,
                    "professional_id": user.professional_data.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.name,
                    "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
                }
            )
    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": users_list,
                "pagination": {
                    "total": users_paginated.total,
                    "pages": users_paginated.pages,
                    "prev_num": users_paginated.prev_num,
                    "next_num": users_paginated.next_num,
                    "current_page": users_paginated.page,
                    "per_page": users_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )

def search_users_controller():
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

    user_results = User.query.filter(
        (User.name.ilike(f'%{query}%')) | 
        (User.email.ilike(f'%{query}%')) | 
        (User.username.ilike(f'%{query}%'))
    )
    user_results = user_results.order_by(get_sorting_field(sort_by, direction))
    user_results_paginated = user_results.paginate(page=page, per_page=per_page, )

    
    users = [{'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role.name.capitalize(), 'date_created': user.date_created.strftime('%B %d, %Y %I:%M %p')} for user in user_results_paginated.items]
    return jsonify(
        {
            "success": True,
            "data": users,
            "pagination": {
                "total": user_results_paginated.total,
                "pages": user_results_paginated.pages,
                "prev_num": user_results_paginated.prev_num,
                "next_num": user_results_paginated.next_num,
                "current_page": user_results_paginated.page,
                "per_page": user_results_paginated.per_page,
            },
            "sort_by": sort_by,
            "direction": direction,
        }
    ), 200

