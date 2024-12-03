from datetime import datetime

from flask import jsonify, request
from sqlalchemy import asc, desc
from sqlalchemy.orm import aliased
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

from app.models import Service, Category, db, ServiceRequest, Customer, Professional, User, ServiceStatus, Review
from app.config import PaginationConfig
from app.models.notification import Notification
from app.models.user import Role
import pytz

from app.utils.helpers import validate_fields

# Utility function for dynamic sorting
def get_sorting_field(sort_by, direction, customer_user, professional_user):
    valid_sort_fields = {
        "id": ServiceRequest.id,
        "start_date": ServiceRequest.start_date,
        "total_days": ServiceRequest.start_date,
        "hours_per_day": ServiceRequest.start_date,
        "total_cost": ServiceRequest.total_cost,
        "service_status": ServiceRequest.service_status,
        "service_name": Service.name,
        "customer_name": customer_user.name,
        "customer_pincode": customer_user.name,
        "professional_name": professional_user.name,
        "date_created": ServiceRequest.date_created,
    }

    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)



def get_service_requests_controller(c_user=None):
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
    status = request.args.get("status", "").upper()
    if status not in ["REQUESTED", "ASSIGNED", "CLOSED", "REJECTED", ""]:
        raise BadRequest("Invalid status. Use 'REQUESTED', 'ASSIGNED', 'CLOSED', 'REJECTED' ")
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    query = (
        db.session.query(ServiceRequest)
        .join(Service, Service.id == ServiceRequest.service_id)
        .join(Customer, Customer.id == ServiceRequest.customer_id)
        .join(customer_user, Customer.user_id == customer_user.id)
        .join(professional_user, Professional.user_id == professional_user.id)
        .join(
            Professional, Professional.id == ServiceRequest.professional_id
        )
    )
    if c_user:
        if c_user.professional_data:
            query = query.filter(ServiceRequest.professional_id == c_user.professional_data.id)
        elif c_user.customer_data:
            query = query.filter(ServiceRequest.customer_id == c_user.customer_data.id)
    if status:
        
        query = query.order_by(
            get_sorting_field(sort_by, direction, customer_user, professional_user)
        ).filter(ServiceRequest.service_status == status)
    else:
        
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
                    "pincode": service_request.customer.user.pincode,
                },
                "professional": {
                    "id": service_request.professional.id,
                    "name": service_request.professional.user.name,
                    "service_price": service_request.professional.service_price,
                },
                "review": service_request.review_id,
                "start_date": service_request.start_date.strftime(
                    "%B %d, %Y"
                ),
                "total_days": service_request.total_days,
                "hours_per_day": service_request.hours_per_day,
                "total_cost": service_request.total_cost,
                "date_of_completion": service_request.date_of_completion.strftime("%b %d, %Y %I:%M %p") if service_request.date_of_completion else None,
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
    # Return successful response with metadata
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
                "status": status,
                "direction": direction,
            }
        ),
        200,
    )



def create_service_request_controller(c_user=None):
    data = request.get_json()
    # Required fields validation
    service_id = data.get("service_id")
    customer_id = data.get("customer_id")
    professional_id = data.get("professional_id")
    total_days = data.get("total_days")
    remarks = data.get("remarks")
    hours_per_day = data.get("hours_per_day")
    start_date = data.get("start_date")

    validate_fields(data, [
        ('service_id', int),
        ('customer_id', int),
        ('professional_id', int),
        ('total_days', int),
        ('hours_per_day', int),
        ('start_date', datetime),
        ('remarks', str),
    ])

    start_date = datetime.fromisoformat(start_date)

    if c_user is not None and c_user.customer_data and c_user.customer_data.id != customer_id:
        raise Forbidden

    professional_service_id = Professional.query.get(professional_id).service_id
    if service_id != professional_service_id:
        raise BadRequest(f"Professional with ID {professional_id} doesn't offer this service")
    
    
    professional = db.session.query(Professional).filter_by(id=professional_id).first()
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    service = db.session.query(Service).filter_by(id=service_id).first()

    if professional:
        # Calculate the total cost based on total_days, hours_per_day, and professional's service price
        total_cost = total_days * hours_per_day * professional.service_price
    else:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")
    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")
    
    new_service_request = ServiceRequest(
        service_id=service_id,
        customer_id=customer_id,
        professional_id=professional_id,
        total_days=total_days,
        hours_per_day=hours_per_day,
        total_cost=total_cost,
        start_date=start_date,
        remarks=remarks,
    )

    db.session.add(new_service_request)
    db.session.commit()
    
    # Notify admins
    admins = User.query.filter_by(role=Role.ADMIN).all()
    for admin in admins:
        notification = Notification(
            message="New Service Request",
            link=f"/admin/service_request/{new_service_request.id}",
            user_id=admin.id
        )
        db.session.add(notification)
    
    # Notify the professional
    professional = db.session.query(Professional).filter_by(id=new_service_request.professional_id).first()
    if professional:
        professional_notification = Notification(
            message="New Service Request",
            link=f"/professional/service_request/{new_service_request.id}",
            user_id=professional.user_id
        )
        db.session.add(professional_notification)

    customer = db.session.query(Customer).filter_by(id=new_service_request.customer_id).first()
    if customer:
        customer_notification = Notification(
            message="New Service Request",
            link=f"/service_request/{new_service_request.id}",
            user_id=customer.user_id
        )
        db.session.add(customer_notification)
    
    db.session.commit()

    service_request_data = {column.name: getattr(new_service_request, column.name) for column in ServiceRequest.__table__.columns}
    service_request_data['service_status'] = new_service_request.service_status.name

    return (
        jsonify(
            {
                "success": True,
                "message": "Service request created successfully",
                "data": service_request_data,
            }
        ),
        201,
    )




def delete_service_request_controller(service_request_id):

    service_request = ServiceRequest.query.get(service_request_id)
    if not service_request:
        raise NotFound(f"Service Request with ID {service_request_id} not found.")

    try:
        db.session.delete(service_request)
        db.session.commit()
        return (
            jsonify(success=True, message="Service Request deleted successfully"),
            200,
        )
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete Service Request with ID {service_request_id}")



def get_service_request_controller(service_request_id, c_user=None):
    if not service_request_id or not isinstance(service_request_id, int):
        raise BadRequest("Invalid service request ID provided.")

    service_request = ServiceRequest.query.filter_by(id=service_request_id).first()
    if not service_request:
        raise NotFound(f"Service Request with ID {service_request_id} not found.")

    if c_user:
        if c_user.customer_data and c_user.customer_data.id != service_request.customer_id:
            raise Forbidden
        elif c_user.professional_data and c_user.professional_data.id != service_request.professional_id:
            raise Forbidden
    
    customer_user = aliased(User)
    professional_user = aliased(User)
    service_request = (
        db.session.query(ServiceRequest)
        .join(Service, Service.id == ServiceRequest.service_id)
        .join(Customer, Customer.id == ServiceRequest.customer_id)
        .join(customer_user, Customer.user_id == customer_user.id)
        .join(professional_user, Professional.user_id == professional_user.id)
        .join(
            Professional, Professional.id == ServiceRequest.professional_id
        ).filter(ServiceRequest.id==service_request_id).first()
    )

    if not service_request:
        raise NotFound(f"Service Request with ID {service_request} not found.")
    category = db.session.query(Category, Service).join(Service, Service.category_id == Category.id).filter(Service.id==service_request.service.id).first()
    review = Review.query.filter_by(service_request_id=service_request_id).first()
    if category:
        category_name = category.Category.name
        category_id = category.Category.id
    service_request_detail = {
        "id": service_request.id,
        "service": {
            "id": service_request.service.id,
            "name": service_request.service.name,
            "price": service_request.service.price,
            "image": service_request.service.image,
            "description": service_request.service.description,
            "category_name": category_name,
            "category_id": category_id,
        },
        "customer": {
            "id": service_request.customer.id,
            "name": service_request.customer.user.name,
            "image": service_request.customer.user.profile_image,
            "phone": service_request.customer.user.phone,
            "email": service_request.customer.user.email,
        },
        "professional": {
            "id": service_request.professional.id,
            "name": service_request.professional.user.name,
            "image": service_request.professional.user.profile_image,
            "email": service_request.professional.user.email,
            "phone": service_request.professional.user.phone,
            "service_price": service_request.professional.service_price,
        },
    "review": {
        "id": review.id,
        "value": review.value,
        "date_created": review.date_created.strftime("%B %d, %Y %I:%M %p"),
        "description": review.description,
    } if review else None,
        "start_date": service_request.start_date.strftime("%B %d, %Y"),
        "total_days": service_request.total_days,
        "hours_per_day": service_request.hours_per_day,
        "total_cost": service_request.total_cost,
        "date_of_completion": service_request.date_of_completion.strftime("%B %d, %Y %I:%M %p") if service_request.date_of_completion else "NA",
        "service_status": service_request.service_status.name,
        "remarks": service_request.remarks,
        "date_created": service_request.date_created.strftime("%B %d, %Y %I:%M %p"),
        "date_updated": service_request.date_updated.strftime("%B %d, %Y %I:%M %p"),
    }
    return jsonify({"success": True, "data": service_request_detail}), 200


def edit_service_request_controller(service_request_id, c_user=None):
    if not service_request_id or not isinstance(service_request_id, int):
        raise BadRequest("Invalid service request ID provided.")
    service_request = ServiceRequest.query.filter_by(id=service_request_id).first()
    if not service_request:
        raise NotFound(f"Service Request with ID {service_request_id} not found.")

    if c_user:
        if c_user.customer_data and c_user.customer_data.id != service_request.customer_id:
            raise Forbidden
        elif c_user.professional_data and c_user.professional_data.id != service_request.professional_id:
            raise Forbidden
    
    data = request.get_json()
    service_id = data.get("service_id")
    if not service_id:
        data['service_id']= service_request.service_id
        service_id= service_request.service_id

    customer_id = data.get("customer_id")
    if not customer_id:
        data['customer_id']= service_request.customer_id
        customer_id= service_request.customer_id

    professional_id = data.get("professional_id")
    if not professional_id:
        data['professional_id']= service_request.professional_id
        professional_id= service_request.professional_id

    review_id = data.get("review_id")
    if not review_id:
        data['review_id']= service_request.review_id
        review_id = service_request.review_id

    total_days = data.get("total_days")
    if not total_days:
        data['total_days']= service_request.total_days
        total_days = service_request.total_days
        
    remarks = data.get("remarks")
    remarksx = data.get("remarks")
    if not remarks:
        data['remarks']= service_request.remarks
        remarks = service_request.remarks

    service_status = data.get("service_status")
    if not data.get("service_status"):
        data['service_status'] = service_request.service_status.name
        service_status = service_request.service_status.name

    hours_per_day = data.get("hours_per_day")
    if not data.get("hours_per_day"):
        data['hours_per_day'] = service_request.hours_per_day
        hours_per_day = service_request.hours_per_day

    start_date = data.get("start_date")
    if not data.get("start_date"):
        data['start_date'] = service_request.start_date.date().isoformat()
        start_date = service_request.start_date.date().isoformat()
    validate_fields(data, [
        ('service_id', int),
        ('customer_id', int),
        ('professional_id', int),
        ('total_days', int),
        ('hours_per_day', int),
        ('start_date', datetime),
        ('service_status', str),
        ('remarks', str),
    ])

    start_date = datetime.fromisoformat(start_date)

    professional_service_id = Professional.query.get(professional_id).service_id
    if service_id != professional_service_id:
        raise BadRequest(f"Professional with ID {professional_id} doesn't offer this service")

    
    professional = db.session.query(Professional).filter_by(id=professional_id).first()
    customer = db.session.query(Customer).filter_by(id=customer_id).first()
    service = db.session.query(Service).filter_by(id=service_id).first()

    if professional:
        # Calculate the total cost based on total_days, hours_per_day, and professional's service price
        total_cost = total_days * hours_per_day * professional.service_price
    else:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")
    if not service:
        raise NotFound(f"Service with ID {service_id} not found.")

    if c_user:
        if remarksx:
            service_request.remarks = remarksx
            service_request.date_updated = datetime.now(pytz.timezone('Asia/Kolkata'))
            db.session.commit()
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Remarks updated successfully",
                    }
                ),
                200,
            )
        if c_user.customer_data:
            if data.get("service_status") == "CLOSED" and data.get("service_status") != service_request.service_status.name:
                service_request.service_status = ServiceStatus.CLOSED
                service_request.date_of_completion = datetime.now(pytz.timezone('Asia/Kolkata'))
                service_request.date_updated = datetime.now(pytz.timezone('Asia/Kolkata'))
                db.session.commit()
                return (
                    jsonify(
                        {
                            "success": True,
                            "message": "Service status updated successfully",
                        }
                    ),
                    200,
                )
            elif data.get("start_date"):
                if service_request.service_status == ServiceStatus.REQUESTED:
                    service_request.start_date = start_date
                    service_request.date_updated = datetime.now(pytz.timezone('Asia/Kolkata'))
                    db.session.commit()
                    return (
                        jsonify(
                            {
                                "success": True,
                                "message": "Start Date updated successfully",
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {
                                "success": False,
                                "message": "Cannot edit start_date",
                            }
                        ),
                        400,
                    )
            else:
                raise Forbidden("service_status and start_date can only be changed")
            
        elif c_user.professional_data:
            if data.get("service_status") == "ASSIGNED":
                service_request.service_status = ServiceStatus.ASSIGNED
            elif data.get("service_status") == "REJECTED":
                service_request.service_status = ServiceStatus.REJECTED
            elif data.get("service_status") == "CLOSED":
                service_request.service_status = ServiceStatus.CLOSED
                service_request.date_of_completion = datetime.now(pytz.timezone('Asia/Kolkata'))
            else:
                raise Forbidden("you can change the service_status to 'ASSIGNED', 'REJECTED' or 'CLOSED'")
            service_request.date_updated = datetime.now(pytz.timezone('Asia/Kolkata'))
            db.session.commit()
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Service status updated successfully",
                    }
                ),
                200,
            )

        

    else:
        service_request.service_id = service_id
        service_request.customer_id = customer_id
        service_request.professional_id = professional_id
        service_request.review_id = review_id
        service_request.total_days = total_days
        service_request.remarks = remarks
        service_request.total_cost = total_cost
        service_request.date_of_completion = datetime.now(pytz.timezone('Asia/Kolkata'))
        
        if service_status == "ASSIGNED":
            service_request.service_status = ServiceStatus.ASSIGNED
        elif service_status == "REQUESTED":
            service_request.service_status = ServiceStatus.REQUESTED
        elif service_status == "CLOSED":
            service_request.service_status = ServiceStatus.CLOSED
            service_request.date_of_completion = datetime.now(pytz.timezone('Asia/Kolkata'))
        elif service_status == "REJECTED":
            service_request.service_status = ServiceStatus.REJECTED
        service_request.date_updated = datetime.now(pytz.timezone('Asia/Kolkata'))
        
    
    service_request.hours_per_day = hours_per_day
        
    db.session.commit()
    return (
        jsonify(
            {
                "success": True,
                "message": "Service request updated successfully",
            }
        ),
        200,
    )



def search_service_requests_controller(c_user=None):
    customer_user = aliased(User)
    professional_user = aliased(User)
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
    status = request.args.get("status", "").upper()

    if status not in ["REQUESTED", "ASSIGNED", "CLOSED", "REJECTED", ""]:
        raise BadRequest("Invalid status. Use 'REQUESTED', 'ASSIGNED', 'CLOSED', 'REJECTED' ")
    
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    # Date range filters
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
    except ValueError:
        raise BadRequest("Invalid date format. Use 'YYYY-MM-DD'.")

    query_filter = (
        (customer_user.name.ilike(f"%{query}%"))
        | (customer_user.email.ilike(f"%{query}%"))
        | (professional_user.name.ilike(f"%{query}%"))
        | (professional_user.email.ilike(f"%{query}%"))
        | (Service.name.ilike(f"%{query}%"))
        | (ServiceRequest.total_cost.ilike(f"%{query}%"))
        | (ServiceRequest.remarks.ilike(f"%{query}%"))
        | (ServiceRequest.service_status.ilike(f"%{query}%"))
    )

    service_request_results = (
        db.session.query(ServiceRequest)
        .join(Service, Service.id == ServiceRequest.service_id)
        .join(Customer, Customer.id == ServiceRequest.customer_id)
        .join(customer_user, Customer.user_id == customer_user.id)
        .join(professional_user, Professional.user_id == professional_user.id)
        .join(Professional, Professional.id == ServiceRequest.professional_id)
        .filter(query_filter)
    )

    if c_user:
        if c_user.professional_data:
            service_request_results = service_request_results.filter(ServiceRequest.professional_id == c_user.professional_data.id)
        elif c_user.customer_data:
            service_request_results = service_request_results.filter(ServiceRequest.customer_id == c_user.customer_data.id)

    # Apply the status filter only if status is provided
    if status:
        service_request_results = service_request_results.filter(ServiceRequest.service_status==status)

    # Apply date range filters
    if start_date:
        service_request_results = service_request_results.filter(ServiceRequest.start_date >= start_date)
    if end_date:
        service_request_results = service_request_results.filter(ServiceRequest.start_date <= end_date)
    
    service_request_results = service_request_results.order_by(
        get_sorting_field(sort_by, direction, customer_user, professional_user)
    )
    
    service_request_results_paginated = service_request_results.paginate(
        page=page, per_page=per_page
    )

    service_requests = [
        {
            "id": service_request.id,
            "service": service_request.service.name,
            "customer": service_request.customer.user.name,
            "professional": service_request.professional.user.name,
            "remarks": service_request.remarks,
            "total_cost": service_request.total_cost,
            "total_days": service_request.total_days,
            "customer_pincode": service_request.customer.user.pincode,
            "hours_per_day": service_request.hours_per_day,
            "date_created": service_request.date_created.strftime("%B %d, %Y %I:%M %p"),
            "start_date": service_request.start_date.strftime("%B %d, %Y"),
            "status": service_request.service_status.name.capitalize(),
        }
        for service_request in service_request_results_paginated.items
    ]
    return (
        jsonify(
            {
                "success": True,
                "data": service_requests,
                "pagination": {
                    "total": service_request_results_paginated.total,
                    "pages": service_request_results_paginated.pages,
                    "prev_num": service_request_results_paginated.prev_num,
                    "next_num": service_request_results_paginated.next_num,
                    "current_page": service_request_results_paginated.page,
                    "per_page": service_request_results_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )
