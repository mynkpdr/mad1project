from datetime import datetime
import pytz

from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Conflict
from app.models import db, Review, ServiceRequest, User, Role, Customer
from app.models.professional import Professional
from app.models.service_request import ServiceStatus
from app.config import PaginationConfig
from app.utils.helpers import validate_fields

from sqlalchemy import asc, desc
from sqlalchemy.orm import aliased

# Utility function for dynamic sorting
def get_sorting_field(sort_by, direction, professional_user, customer_user):
    valid_sort_fields = {
        "id": Review.id,
        "professional_name": professional_user.name,
        "customer_name": customer_user.name,
        "value": Review.value,
        "description": Review.description,
        "date_created": Review.date_created,
    }

    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)



def create_review_controller(c_user=None):

    data = request.get_json()
    
    professional_id = data.get("professional_id")
    customer_id = data.get("customer_id")
    service_request_id = data.get("service_request_id")
    description = data.get("description")
    value = data.get("value")

    validate_fields(data, [
        ('professional_id', int),
        ('customer_id', int),
        ('service_request_id', int),
        ('value', int),
    ])

    service_request = ServiceRequest.query.filter_by(id=service_request_id).first()
    if c_user is not None and (c_user.customer_data.id != customer_id or service_request.professional_id != professional_id):
        raise Forbidden
    
    old_review = Review.query.filter_by(professional_id=professional_id, customer_id=customer_id, service_request_id=service_request_id).first()
    if old_review:
        raise Conflict("You cannot add more than one review for the same service request")

    new_review = Review(
        professional_id=professional_id,
        customer_id=customer_id,
        service_request_id=service_request_id,
        description=description,
        value=value,
        date_created=datetime.now(pytz.timezone("Asia/Kolkata")),
    )

    db.session.add(new_review)

    if service_request:
        if service_request.service_status != ServiceStatus.CLOSED:
            raise ValueError("Review can only be added if the service status is CLOSED.")
        professional = Professional.query.get(service_request.professional_id)
        if professional:
            reviews = Review.query.filter_by(professional_id=service_request.professional_id).all()
            if reviews:
                average_rating = round(sum(review.value for review in reviews) / len(reviews), 2)
                professional.rating = average_rating
            else:
                professional.rating = value
        service_request.review_id = new_review.id
    db.session.commit()

    review_data = {column.name: getattr(new_review, column.name) for column in Review.__table__.columns}
    
    return (
        jsonify(
            {
                "success": True,
                "message": "Review created successfully",
                "data": review_data,
            }
        ),
        201,
    )


def delete_review_controller(review_id, c_user=None):
    review = db.session.query(Review).filter_by(id=review_id).first()

    if not review:
        raise NotFound(f"Review with ID {review_id} not found.")

    if c_user is not None and review.customer_id != c_user.customer_data.id:
        raise Forbidden
    try:
        service_request = ServiceRequest.query.filter_by(review_id=review_id).first()
        db.session.delete(review)
        db.session.commit()
        
        if service_request:
            professional = Professional.query.get(service_request.professional_id)
            if professional:
                reviews = Review.query.filter_by(professional_id=professional.id).all()
                if reviews:
                    average_rating = round(sum(review.value for review in reviews) / len(reviews), 2)
                    professional.rating = average_rating
                else:
                    professional.rating = 0
                db.session.commit()
        return jsonify(success=True, message="Review deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete review with ID {review_id}")


def get_reviews_controller(c_user=None):
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
    professional_user = aliased(User)
    customer_user = aliased(User)

    query = db.session.query(Review).join(Customer, Customer.id == Review.customer_id).join(Professional, Professional.id == Review.professional_id).join(customer_user, Customer.user_id == customer_user.id).join(professional_user, Professional.user_id==professional_user.id)
    if c_user:
        if c_user.role == Role.PROFESSIONAL:
            query = query.filter(Review.professional_id==c_user.professional_data.id)
        elif c_user.role == Role.CUSTOMER:
            query = query.filter(Review.customer_id==c_user.customer_data.id)

    query = query.order_by(get_sorting_field(sort_by, direction, professional_user, customer_user))

    
    reviews_paginated = query.paginate(page=page, per_page=per_page)
    
    reviews_list = []
    for review in reviews_paginated.items:
        reviews_list.append(
            {
                "id":review.id,
                "value":review.value,
                "customer": {
                    "id":review.customer.id,
                    "user_id":review.customer.user.id,
                    "name":review.customer.user.name,
                    "profile_image":review.customer.user.profile_image,
                },
                "service_request": {
                    "id":review.service_request_id
                },
                "professional": {
                    "id":review.professional.id,
                    "user_id":review.professional.user.id,
                    "name":review.professional.user.name,
                    "profile_image":review.professional.user.profile_image,
                },
                "description":review.description,
                "date_created":review.date_created.strftime(
                    "%B %d, %Y %I:%M %p"
                ),
            }
        )

    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": reviews_list,
                "pagination": {
                    "total": reviews_paginated.total,
                    "pages": reviews_paginated.pages,
                    "prev_num": reviews_paginated.prev_num,
                    "next_num": reviews_paginated.next_num,
                    "current_page": reviews_paginated.page,
                    "per_page": reviews_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )