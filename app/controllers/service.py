from datetime import datetime
import pytz

from flask import jsonify, request
from sqlalchemy import asc, desc, text
from sqlalchemy.orm import aliased
from werkzeug.exceptions import BadRequest, NotFound

from app.models import Service, Category, db, ServiceRequest, User, Customer, Professional, Review, ServiceStatus, Role
from app.config import PaginationConfig

from app.utils.helpers import validate_fields

# Utility function for dynamic sorting
def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": Service.id,
        "name": Service.name,
        "price": Service.price,
        "category": Category.name,
        "description": Service.description,
        "date_created": Service.date_created,
    }

    if sort_by == "starting_professional_price":
        sort_field = db.func.min(Professional.service_price)
    else:
        if sort_by not in valid_sort_fields:
            raise BadRequest(
                f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
            )
        sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)


def get_services_controller():
    # Get and validate query parameters
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", Service.query.count(), type=int)
    sort_by = request.args.get(
        "sort_by", PaginationConfig.DEFAULT_SORT_BY
    ).lower()
    direction = request.args.get(
        "direction", PaginationConfig.DEFAULT_DIRECTION
    ).lower()
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    query = db.session.query(Service, Category).join(
        Category, Service.category_id == Category.id
    )

    if sort_by == "starting_professional_price":
        query = (
            query.outerjoin(Professional, Service.id == Professional.service_id)
            .group_by(Service.id)
            .having(db.func.min(Professional.service_price) > 0)  # Only include services with professionals having prices
            .order_by(get_sorting_field(sort_by, direction))
        )
        
    
    query = query.order_by(get_sorting_field(sort_by, direction))
    
    services_paginated = query.paginate(page=page, per_page=per_page)
    
    services_list = []
    for service, category in services_paginated.items:
        # Query the professionals associated with each service
        professionals = (
            db.session.query(Professional)
            .join(Service, Service.id == Professional.service_id)
            .filter(Professional.service_id == service.id)
            .all()
        )
        
        professionals_list = []
        for professional in professionals:
            # Count the total number of reviews for each professional
            total_reviews = db.session.query(Review).filter_by(professional_id=professional.id).count()
            
            professionals_list.append(
                {
                    "id": professional.id,
                    "name": professional.user.name,
                    "email": professional.user.email,
                    "price": professional.service_price,
                    "profile_image": professional.user.profile_image,
                    "rating": float(professional.rating),
                    "total_reviews": total_reviews,
                }
            )
        lowest_service_price = db.session.query(db.func.min(Professional.service_price)).filter(Professional.service_id == service.id).scalar()
        services_list.append(
            {
                "id": service.id,
                "name": service.name,
                "price": service.price,
                "starting_professional_price": lowest_service_price,
                "image": service.image,
                "description": service.description,
                "category": {"id": category.id, "name": category.name},
                "date_created": service.date_created.strftime("%B %d, %Y %I:%M %p"),
                "professionals": professionals_list,
                "total_service_requests": ServiceRequest.query.filter_by(service_id=service.id).count(),
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



def create_service_controller():

    data = request.get_json()
    
    name = data.get("name")
    price = data.get("price")
    description = data.get("description")
    category_id = data.get("category_id")
    image = data.get("image", "default.jpg")

    validate_fields(data, [
        ('name', str),
        ('price', int),
        ('category_id', int),
        ('description', str),
    ])

    if not Category.query.get(category_id):
        raise NotFound(f"Category with ID {category_id} not found.")

    new_service = Service(
        name=name,
        price=price,
        description=description,
        category_id=category_id,
        image=image,
        date_created=datetime.now(pytz.timezone("Asia/Kolkata")),
    )

    db.session.add(new_service)
    db.session.commit()

    service_data = {column.name: getattr(new_service, column.name) for column in Service.__table__.columns}

    return (
        jsonify(
            {
                "success": True,
                "message": "Service created successfully",
                "data": service_data,
            }
        ),
        201,
    )



def get_service_controller(service_id):

    service = (
        db.session.query(Service, Category)
        .join(Category, Service.category_id == Category.id)
        .filter(Service.id == service_id)
        .first()
    )

    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")

    # Get and validate query parameters for professionals
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", PaginationConfig.DEFAULT_PER_PAGE, type=int)
    sort_by = request.args.get("sort_by", 'rating').lower()
    direction = request.args.get("direction", PaginationConfig.DEFAULT_DIRECTION).lower()

    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    professionals_query = db.session.query(Professional).join(User).filter(Professional.service_id==service_id).filter(User.blocked == False)

    
    if sort_by == "rating":
        professionals_query = professionals_query.order_by(
            Professional.rating.desc() if direction == "desc" else Professional.rating
        )
    elif sort_by == "price":
        professionals_query = professionals_query.order_by(
            Professional.service_price.desc() if direction == "desc" else Professional.service_price
        )
    else:
        pass

    professionals_paginated = professionals_query.paginate(page=page, per_page=per_page)

    professionals_list = []
    for professional in professionals_paginated.items:
        total_reviews = db.session.query(Review).filter_by(professional_id=professional.id).count()
        total_service_requests_completed = ServiceRequest.query.filter_by(service_status=ServiceStatus.CLOSED).filter_by(professional_id=professional.id).count()
        professionals_list.append({
            "id": professional.id,
            "name": professional.user.name,
            "image": professional.user.profile_image,
            "address": professional.user.address,
            "about": professional.user.about,
            "price": professional.service_price,
            "total_reviews": total_reviews,
            "rating": professional.rating,
            "total_service_requests_completed": total_service_requests_completed,
        })

    service_data, category_data = service

    service_detail = {
        "id": service_data.id,
        "name": service_data.name,
        "price": service_data.price,
        "professionals": professionals_list,
        "image": service_data.image,
        "description": service_data.description,
        "category": {"id": category_data.id, "name": category_data.name},
        "date_created": service_data.date_created.strftime("%B %d, %Y"),
        "pagination": {
            "total": professionals_paginated.total,
            "pages": professionals_paginated.pages,
            "prev_num": professionals_paginated.prev_num,
            "next_num": professionals_paginated.next_num,
            "current_page": professionals_paginated.page,
            "per_page": professionals_paginated.per_page,
        },
        "sort_by": sort_by,
        "direction": direction,
    }

    return jsonify({"success": True, "data": service_detail}), 200


def delete_service_controller(service_id):

    service = Service.query.get(service_id)
    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")

    try:
        db.session.delete(service)
        db.session.commit()
        return jsonify(success=True, message="Service deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete service with ID {service_id}")



def edit_service_controller(service_id):

    service = Service.query.get(service_id)
    if service is None:
        raise NotFound(f"Service with ID {service_id} not found.")
    
    data = request.get_json()

    name = data.get("name")
    if not name:
        data['name'] = service.name
        name = service.name

    price = data.get("price")
    if not price:
        data['price'] = service.price
        price = service.price

    category_id = data.get("category_id")
    if not category_id:
        data['category_id'] = service.category_id
        category_id = service.category_id

    description = data.get("description")
    if not description:
        data['description'] = service.description
        description = service.description

    image = data.get("image")
    if not image:
        data['image'] = service.image
        image = service.image

    validate_fields(data, [
        ('name', str),
        ('price', int),
        ('category_id', int),
        ('description', str),
    ])


    if not Category.query.get(category_id):
        raise NotFound(f"Category with ID {category_id} not found.")
    service.name = name
    service.price = price
    service.category_id = category_id
    service.description = description
    service.image = image

    try:
        db.session.commit()
        return jsonify(success=True, message="Service updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating service")



def get_service_category_controller(service_id):

    category_detail = db.session.query(Category).join(Service, Service.category_id == Category.id).filter(Service.id == service_id).first()

    if not category_detail:
        raise NotFound(f"Service with ID {service_id} not found.")
    
    category_detail = (
        {
            "id": category_detail.id,
            "name": category_detail.name,
        },
    )

    return jsonify({"success": True, "data": category_detail}), 200



def get_service_service_requests_controller(service_id):
    from .service_request import get_sorting_field

    customer_user = aliased(User)
    professional_user = aliased(User)
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

    service = Service.query.get(service_id)

    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")

    query = (
        db.session.query(ServiceRequest)
        .join(Service, Service.id == ServiceRequest.service_id)
        .join(Customer, Customer.id == ServiceRequest.customer_id)
        .join(customer_user, Customer.user_id == customer_user.id)
        .join(professional_user, Professional.user_id == professional_user.id)
        .join(
            Professional, Professional.id == ServiceRequest.professional_id
        )
    ).filter(Service.id == service_id)
    
    query = query.order_by(
        get_sorting_field(sort_by, direction, customer_user, professional_user)
    )
    
    service_requests_paginated = query.paginate(page=page, per_page=per_page)
    
    service_requests_list = []
    for service_request in service_requests_paginated.items:
        service_requests_list.append(
            {
                "id": service_request.id,
                "service": {
                    "id": service_request.service.id,
                    "name": service_request.service.name,
                    "price": service_request.service.price,
                },
                "customer": {
                    "id": service_request.customer.id,
                    "name": service_request.customer.user.name,
                },
                "professional": {
                    "id": service_request.professional.id,
                    "name": service_request.professional.user.name,
                    "service_price": service_request.professional.service_price,
                },
                "review": service_request.review_id,
                "start_date": service_request.start_date,
                "total_days": service_request.total_days,
                "hours_per_day": service_request.hours_per_day,
                "total_cost": service_request.total_cost,
                "date_of_completion": service_request.date_of_completion,
                "service_status": service_request.service_status.name,
                "remarks": service_request.remarks,
                "date_created": service_request.date_created.strftime(
                    "%B %d, %Y %I:%M %p"
                ),
                "date_updated": service_request.date_updated.strftime(
                    "%B %d, %Y %I:%M %p"
                ),
            }
        )
    return (
        jsonify(
            {
                "success": True,
                "data": service_requests_list,
                "pagination": {
                    "total": service_requests_paginated.total,
                    "pages": service_requests_paginated.pages,
                    "prev_num": service_requests_paginated.prev_num,
                    "next_num": service_requests_paginated.next_num,
                    "current_page": service_requests_paginated.page,
                    "per_page": service_requests_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )

def get_nearby_professionals_controller(c_user, service_id):
    customer_lat = c_user.latitude
    customer_long = c_user.longitude
    service_id = service_id
    data = request.get_json()
    distance_km = data.get('distance_km')

    validate_fields(data, [
        ('distance_km', int),
    ])
    
    # Query for professionals offering the specified service (e.g., plumbing)
    service = Service.query.filter_by(id=service_id).first()
    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")
    # Use raw SQL to calculate the distance using Haversine formula https://en.wikipedia.org/wiki/Haversine_formula
    query = text("""
    SELECT user.id, user.name, user.profile_image, user.latitude, user.longitude, professional.rating,
    professional.service_price, professional.id AS professional_id,
    (6371 * acos(cos(radians(:customer_lat)) * cos(radians(user.latitude)) 
    * cos(radians(user.longitude) - radians(:customer_long)) 
    + sin(radians(:customer_lat)) * sin(radians(user.latitude)))) AS distance
    FROM professional
    JOIN user ON professional.user_id = user.id
    JOIN service ON professional.service_id =service.id
    WHERE professional.service_id = :service_id
    AND user.blocked = False
    AND (6371 * acos(cos(radians(:customer_lat)) * cos(radians(user.latitude)) 
    * cos(radians(user.longitude) - radians(:customer_long)) 
    + sin(radians(:customer_lat)) * sin(radians(user.latitude)))) < :distance_km
    ORDER BY distance;
""")

    professionals = db.session.execute(query, {
        'customer_lat': customer_lat,
        'customer_long': customer_long,
        'service_id': service.id,
        'distance_km': distance_km
    }).fetchall()
    
    result = []
    for row in professionals:
        totalreviews = Review.query.filter(Review.professional_id == row.professional_id).count()
        result.append({
            "user_id": row.id,
            "name": row.name,
            "id": row.professional_id,
            "rating": row.rating,
            "profile_image": row.profile_image,
            "totalreviews": totalreviews,
            "service_name": service.name,
            "service_price": row.service_price,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "distance": row.distance
        })
    return jsonify({"success":True, "data":result}), 200

def get_pincode_professionals_controller(service_id):
    data = request.get_json()
    
    pincode = data.get("pincode")
    
    validate_fields(data, [
        ("pincode", int)
    ])
    professionals = db.session.query(User, Professional, Service).join(Professional, Professional.user_id == User.id).join(Service, Service.id == Professional.service_id).filter(User.pincode == pincode, Service.id==service_id).filter(User.blocked == False).all()

    result = []
    for user, professional, service in professionals:
        totalreviews = Review.query.filter(Review.professional_id == professional.id).count()
        result.append({
            "user_id": user.id,
            "name": user.name,
            "id": professional.id,
            "rating": professional.rating,
            "profile_image": user.profile_image,
            "totalreviews": totalreviews,
            "service_name": service.name,
            "service_price": professional.service_price,
            "latitude": user.latitude,
            "longitude": user.longitude
        })
    return jsonify({"success":True, "data":result}), 200


def search_service_controller():
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

    service_results = (
        db.session.query(Service, Category)
        .join(Service, Service.category_id == Category.id)
        .filter(
            (Service.id.ilike(f"%{query}%"))
            | (Service.name.ilike(f"%{query}%"))
            | (Service.price.ilike(f"%{query}%"))
            | (Category.name.ilike(f"%{query}%"))
            | (Service.description.ilike(f"%{query}%"))
        )
    )

    service_results = service_results.order_by(get_sorting_field(sort_by, direction))
    
    service_results_paginated = service_results.paginate(page=page, per_page=per_page)

    services = [
        {
            "id": service.Service.id,
            "image": service.Service.image,
            "name": service.Service.name,
            "category": service.Category.name,
            "price": service.Service.price,
            "description": f"{service.Service.description}",
        }
        for service in service_results_paginated.items
    ]
    return (
        jsonify(
            {
                "success": True,
                "data": services,
                "pagination": {
                    "total": service_results_paginated.total,
                    "pages": service_results_paginated.pages,
                    "prev_num": service_results_paginated.prev_num,
                    "next_num": service_results_paginated.next_num,
                    "current_page": service_results_paginated.page,
                    "per_page": service_results_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )
