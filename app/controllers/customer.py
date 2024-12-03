from flask import request, jsonify
from sqlalchemy import asc, desc
from werkzeug.exceptions import BadRequest, NotFound, Forbidden, Conflict
import re
from app.utils.helpers import validate_fields
from app.models import User, Customer, Role, db, ServiceRequest, Review, ServiceStatus, Notification
from app.config import PaginationConfig


def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": User.id,
        "name": User.name,
        "email": User.email,
        "date_created": User.date_created,
    }
    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)

def get_customers_controller():
    # Get and validate query parameters
    page = request.args.get("page", PaginationConfig.DEFAULT_PAGE, type=int)
    per_page = request.args.get("per_page", PaginationConfig.DEFAULT_PER_PAGE, type=int)
    sort_by = request.args.get(
        "sort_by", PaginationConfig.DEFAULT_SORT_BY
    ).lower()
    direction = request.args.get(
        "direction", PaginationConfig.DEFAULT_DIRECTION
    ).lower()

    blocked = request.args.get("blocked", "").lower()

    if blocked not in ["true", "false", ""]:
        raise BadRequest("Invalid blocked status. Use either 'true' or 'false ")

    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")
    user = User.query.filter(User.role == Role.CUSTOMER)
    user = user.order_by(get_sorting_field(sort_by, direction))

    if blocked == "true":
        user = user.order_by(
            get_sorting_field(sort_by, direction)
        ).filter(User.blocked == True)
    elif blocked == "false":
        
        user = user.order_by(
            get_sorting_field(sort_by, direction)
        ).filter(User.blocked == False)
    else:
        
        user = user.order_by(
            get_sorting_field(sort_by, direction)
        )

    
    customers_paginated = user.paginate(page=page, per_page=per_page)
    
    customers_list = []
    for customer in customers_paginated.items:
        customers_list.append(
            {
                "id": customer.customer_data.id,
                "user_id": customer.id,
                "name": customer.name,
                "blocked": customer.blocked,
                "email": customer.email,
                "date_created": customer.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )
    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": customers_list,
                "pagination": {
                    "total": customers_paginated.total,
                    "pages": customers_paginated.pages,
                    "prev_num": customers_paginated.prev_num,
                    "next_num": customers_paginated.next_num,
                    "current_page": customers_paginated.page,
                    "per_page": customers_paginated.per_page,
                },
                "blocked": blocked,
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )

def edit_customer_controller(customer_id, c_user=None):
    customer = Customer.query.get(customer_id)
    if customer is None:
        raise NotFound(f"Customer with ID {customer_id} not found.")

    if customer and c_user is not None and c_user.customer_data.id != customer.id:
        raise Forbidden
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided.")
    

    name = data.get("name")
    if not name:
        data['name'] = customer.user.name
        name = customer.user.name

    username = data.get("username")
    if not username:
        data['username'] = customer.user.username
        username = customer.user.username

    email = data.get("email")
    if not email:
        data['email'] = customer.user.email
        email = customer.user.email

    phone = data.get("phone")
    if not phone:
        data['phone'] = customer.user.phone
        phone = customer.user.phone

    about = data.get("about")
    if not about:
        data['about'] = customer.user.about
        about = customer.user.about

    blocked = data.get("blocked")
    if not blocked:
        data['blocked'] = customer.user.blocked
        blocked = customer.user.blocked

    address = data.get("address")
    if not address:
        data['address'] = customer.user.address
        address = customer.user.address

    pincode = data.get("pincode")
    if not pincode:
        data['pincode'] = customer.user.pincode
        pincode = customer.user.pincode

    latitude = data.get("latitude")
    if not latitude:
        data['latitude'] = customer.user.latitude
        latitude = customer.user.latitude

    longitude = data.get("longitude")
    if not longitude:
        data['longitude'] = customer.user.longitude
        longitude = customer.user.longitude

    profile_image = data.get("profile_image")
    if not profile_image:
        data['profile_image'] = customer.user.profile_image
        profile_image = customer.user.profile_image

    new_password = data.get("new_password")
    current_password = data.get("current_password")

    validate_fields(data, [
        ('name', str),
        ('email', str),
        ('username', str),
        ('phone', str),
        ('pincode', int),
        ('blocked', bool),
    ], )

    if User.query.filter_by(username=username).first() and username != customer.user.username:
        raise Conflict(message="Username already exists")
    
    if User.query.filter_by(email=email).first() and email != customer.user.email:
        raise Conflict(message="Email already exists")

    customer.user.name = name
    customer.user.username = username
    customer.user.email = email
    customer.user.phone = phone
    customer.user.about = about
    customer.user.blocked = blocked
    customer.user.address = address
    customer.user.profile_image = profile_image
    customer.user.pincode = pincode
    customer.user.latitude = latitude
    customer.user.longitude = longitude
    
    if new_password and current_password:
        validate_fields(data, [
            ('new_password', str),
            ('current_password', str),
        ], )
        # Check if the current password is correct
        if customer.user and customer.user.check_password(customer.user.email, current_password):
            if not customer.user.check_password(customer.user.email, new_password):
                # Update the password
                customer.user.set_password(new_password)
                
                try:
                    db.session.commit()
                    return jsonify(success=True, message="Password changed successfully"), 200
                except Exception as e:
                    db.session.rollback()
                    raise Exception("Error changing Password")
            else:
                raise Conflict("Current password cannot be same as old password.")
        else:
            raise BadRequest("Current password is incorrect.")
    elif (new_password and not current_password) or (current_password and not new_password):
        validate_fields(data, [
            ('new_password', str),
            ('current_password', str),
        ], )
    try:
        db.session.commit()
        return jsonify(success=True, message="Customer updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating customer")

def create_customer_controller():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    phone = data.get('phone')
    address = data.get('address', '')
    pincode = data.get('pincode')
    about = data.get('about')
    latitude = data.get('lat', '')
    longitude = data.get('lng', '')
    profile_image = data.get('profile_image', 'default.jpg')
    password = data.get('password')

    validate_fields(data, [
        ('name', str),
        ('email', str),
        ('username', str),
        ('phone', str),
        ('password', str),
        ('pincode', int),
    ], )
    
    # Check if email or username exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        raise Conflict("email or username already in use")

    filename = profile_image
    new_user = User(name=name, email=email, username=username, phone=phone,
                    address=address, pincode=pincode, latitude=latitude, about=about,
                    longitude=longitude, profile_image=filename, role="CUSTOMER", password=password)
    db.session.add(new_user)
    db.session.commit()

    new_customer = Customer(user_id=new_user.id)
    db.session.add(new_customer)
    db.session.commit()
    # Notify admins
    admins = User.query.filter_by(role=Role.ADMIN).all()
    for admin in admins:
        notification = Notification(message=f"New Customer: {new_user.name}",
                                         link=f"/admin/customer/{new_user.id}", user_id=admin.id)
        db.session.add(notification)
    db.session.commit()

    user_data = {column.name: getattr(new_user, column.name) for column in User.__table__.columns}
    customer_data = {column.name: getattr(new_customer, column.name) for column in Customer.__table__.columns}

    user_data['role'] = new_user.role.name
    user_data.pop('password')

    # Combine user and customer data into a single response
    response_data = {
        "user": user_data,
        "customer": customer_data
    }

    return jsonify(
        {
            "success": True,
            "message": "Customer account created successfully",
            "data": response_data
        }
    ), 201

def delete_customer_controller(customer_id):

    customer = Customer.query.get(customer_id)
    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")
    user = User.query.get(customer.user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=True, message="Customer deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete customer with ID {customer_id}")

def block_customer_controller(customer_id):
    # Retrieve the service by ID
    customer = Customer.query.get(customer_id)
    if customer is None:
        raise NotFound(f"Customer with ID {customer_id} not found.")
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided.")
    block = data.get("block", customer.user.blocked)
    customer.user.blocked = block

    try:
        db.session.commit()
        if str(block) == "True":
            return jsonify(success=True, message="Customer is now blocked"), 200
        elif str(block) == "False":
            return jsonify(success=True, message="Customer is now active"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating customer")

def get_customer_profile_controller(customer_id):

    customer = Customer.query.filter_by(id = customer_id).first()

    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")

    user = customer.user

    recent_reviews = Review.query.filter_by(customer_id=customer_id).order_by(Review.date_created).limit(3).all()

    recent_reviews_list = [
        {
            "id": review.id,
            "customer_id": review.customer_id,
            "customer_name": user.name,
            "customer_image": user.profile_image,
            "professional_name": review.professional.user.name,
            "service_request_id": review.service_request_id,
            "description": review.description,
            "value": review.value,
            "date_created": review.date_created.strftime("%B %d, %Y %I:%M %p"),
        }
        for review in recent_reviews
    ]

    profile_data = {
        "customer": {
            "id": customer_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "username": user.username,
            "about": user.about,
            "profile_image": user.profile_image,
            "address": user.address,
            "pincode": user.pincode,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "role": "Customer",
            "last_login": user.last_login,
            "blocked": user.blocked,
            "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
            "recent_reviews":recent_reviews_list
        }
    }

    return jsonify({"success": True, "data": profile_data}), 200

def get_customer_controller(customer_id, c_user=None):

    customer = Customer.query.filter_by(id = customer_id).first()

    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")

    user = customer.user


    if customer and c_user is not None and c_user.customer_data.id != customer.id:
        raise Forbidden

    recent_service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).order_by(ServiceRequest.date_created.desc()).limit(3).all()
    recent_reviews = db.session.query(Customer, Review).join(Customer, Customer.id == Review.customer_id).filter(Review.customer_id == customer_id).order_by(db.desc(Review.date_created)).limit(3).all()
    recent_service_requests_list = [
        {
            "id": service_request.id,
            "service_id": service_request.service_id,
            "customer_id": service_request.customer_id,
            "review_id": service_request.review_id,
            "start_date": service_request.start_date.strftime("%B %d, %Y %I:%M %p"),
            "total_days": service_request.total_days,
            "hours_per_day": service_request.hours_per_day,
            "total_cost": service_request.total_cost,
            "date_of_completion": service_request.date_of_completion if service_request.date_of_completion else None,
            "service_status": service_request.service_status.name,
            "remarks": service_request.remarks,
            "date_created": service_request.date_created.strftime("%B %d, %Y %I:%M %p"),
            "date_updated": service_request.date_updated.strftime("%B %d, %Y %I:%M %p"),
        }
        for service_request in recent_service_requests
    ]

    recent_reviews_list = [
        {
            "id": review.id,
            "customer_id": review.customer_id,
            "customer_name": customer.user.name,
            "customer_image": customer.user.profile_image,
            "service_request_id": review.service_request_id,
            "description": review.description,
            "value": review.value,
            "date_created": review.date_created.strftime("%B %d, %Y %I:%M %p"),
        }
        for customer, review in recent_reviews
    ]

    profile_data = {
        "customer": {
            "id": customer_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "username": user.username,
            "about": user.about,
            "profile_image": user.profile_image,
            "address": user.address,
            "pincode": user.pincode,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "role": "Customer",
            "last_login": user.last_login,
            "blocked": user.blocked,
            "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
            "recent_reviews":recent_reviews_list,
            "recent_service_requests":recent_service_requests_list,
            # "closed_service_requests": closed_service_requests,
            # "current_service_requests": current_service_requests,
            # "total_service_requests": total_service_requests
        }
    }

    return jsonify({"success": True, "data": profile_data}), 200

def get_customer_summary_controller(customer_id, c_user=None):


    customer = Customer.query.filter_by(id = customer_id).first()

    if not customer:
        raise NotFound(f"Customer with ID {customer_id} not found.")


    if customer and c_user is not None and c_user.customer_data.id != customer.id:
        raise Forbidden

    total_service_requests = ServiceRequest.query.filter_by(customer_id=customer_id)
    current_service_requests_count = ServiceRequest.query.filter(
                                ServiceRequest.customer_id == customer_id,
                                (ServiceRequest.service_status == ServiceStatus.REQUESTED) | 
                                (ServiceRequest.service_status == ServiceStatus.ASSIGNED)
                            ).count()

    
    closed_service_requests_count = ServiceRequest.query.filter_by(customer_id=customer_id).filter_by(service_status=ServiceStatus.CLOSED).count()
    rejected_service_requests_count = ServiceRequest.query.filter_by(customer_id=customer_id).filter_by(service_status=ServiceStatus.REJECTED).count()
    assigned_service_requests_count = ServiceRequest.query.filter_by(customer_id=customer_id).filter_by(service_status=ServiceStatus.ASSIGNED).count()
    requested_service_requests_count = ServiceRequest.query.filter_by(customer_id=customer_id).filter_by(service_status=ServiceStatus.REQUESTED).count()

    spending_data = {}
    result = []

    if total_service_requests:
        for service_request in total_service_requests:
            if service_request.service_status != ServiceStatus.REJECTED:
                day = service_request.date_created.strftime('%Y-%m-%d')  # e.g., "2024-01-01"
                if day not in spending_data:
                    spending_data[day] = 0
                spending_data[day] += service_request.total_cost
        result = [{'day': day, 'total_spent': total_spent} for day, total_spent in spending_data.items()]

    summary_data = {
        "customer" :{
            "name": customer.user.name,

            "current_service_requests_count" : current_service_requests_count,
            "rejected_service_requests_count" : rejected_service_requests_count,
            "assigned_service_requests_count" : assigned_service_requests_count,
            "requested_service_requests_count" : requested_service_requests_count,
            "closed_service_requests_count" : closed_service_requests_count,

            "spending_data" : result
        }
    }
    # Return the summary data
    return jsonify({"success": True, "data": summary_data}), 200

def search_customers_controller():
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

    blocked = request.args.get("blocked", "").lower()

    if blocked not in ["true", "false", ""]:
        raise BadRequest("Invalid blocked status. Use either 'true' or 'false ")
    
    if direction not in ["asc", "desc"]:
        raise BadRequest("Invalid sort direction. Use 'asc' or 'desc'.")

    # Apply the status filter only if status is provided
    if blocked == "true":
        user_results = User.query.filter(
            (User.role == Role.CUSTOMER) & (
                (User.name.ilike(f'%{query}%')) | 
                (User.email.ilike(f'%{query}%')) | 
                (User.username.ilike(f'%{query}%'))
            )
        ).filter(User.blocked == True)
    elif blocked == "false":
        user_results = User.query.filter(
            (User.role == Role.CUSTOMER) & (
                (User.name.ilike(f'%{query}%')) | 
                (User.email.ilike(f'%{query}%')) | 
                (User.username.ilike(f'%{query}%'))
            )
        ).filter(User.blocked == False)
    else:
        user_results = User.query.filter(
            (User.role == Role.CUSTOMER) & (
                (User.name.ilike(f'%{query}%')) | 
                (User.email.ilike(f'%{query}%')) | 
                (User.username.ilike(f'%{query}%'))
            )
        )

    user_results = user_results.order_by(get_sorting_field(sort_by, direction))
    user_results_paginated = user_results.paginate(page=page, per_page=per_page, )

    
    users = [{'id': user.customer_data.id,
              'user_id': user.id,
              'name': user.name,
              'email': user.email,
              'blocked': user.blocked,
              'image': user.profile_image,
              'about': user.about,
              'role': user.role.name.capitalize(),
              'date_created': user.date_created.strftime('%B %d, %Y %I:%M %p')
              
              } for user in user_results_paginated.items]
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

