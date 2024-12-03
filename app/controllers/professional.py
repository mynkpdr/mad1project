from flask import request, jsonify
from sqlalchemy import asc, desc
from werkzeug.exceptions import NotFound, BadRequest, Forbidden, Conflict
import re
from app.models import Review, User, Service, Category, Customer, Professional, db, ServiceRequest
from app.config import PaginationConfig
from app.models.notification import Notification
from app.models.service_request import ServiceStatus
from app.models.user import Role
from app.utils.helpers import validate_fields


def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": User.id,
        "name": User.name,
        "email": User.email,
        "service_name": Service.name,
        "date_created": User.date_created,
        "active": Professional.active,
    }
    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)

def get_professionals_controller():
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
    professional = db.session.query(Professional, Service, User).join(Service, Professional.service_id == Service.id).join(User, Professional.user_id == User.id)
    professional = professional.order_by(get_sorting_field(sort_by, direction))

    if blocked == "true":
        
        professional = professional.order_by(
            get_sorting_field(sort_by, direction)
        ).filter(User.blocked == True)
    elif blocked == "false":
        
        professional = professional.order_by(
            get_sorting_field(sort_by, direction)
        ).filter(User.blocked == False)
    else:
        
        professional = professional.order_by(
            get_sorting_field(sort_by, direction)
        )

    
    professionals_paginated = professional.paginate(page=page, per_page=per_page)
    
    professionals_list = []
    for professional, service, user in professionals_paginated.items:
        professionals_list.append(
            {
                "id": professional.id,
                "user_id": user.id,
                "service_name": service.name,
                "name": user.name,
                "email": user.email,
                "blocked": user.blocked,
                "active": professional.active,
                "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )
    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": professionals_list,
                "pagination": {
                    "total": professionals_paginated.total,
                    "pages": professionals_paginated.pages,
                    "prev_num": professionals_paginated.prev_num,
                    "next_num": professionals_paginated.next_num,
                    "current_page": professionals_paginated.page,
                    "per_page": professionals_paginated.per_page,
                },
                "blocked": blocked,
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )

def create_professional_controller():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    username = data.get('username')
    phone = data.get('phone')
    address = data.get('address', '')
    about = data.get('about', '')
    pincode = data.get('pincode', '')
    latitude = data.get('lat', '')
    longitude = data.get('lng', '')
    service_id = data.get('service_id', '')
    service_price = data.get('service_price', '')
    experience = data.get('experience', '')
    documents = data.get('documents', '')
    profile_image = data.get('profile_image', '')
    password = data.get('password')

    validate_fields(data, [
        ('name', str),
        ('email', str),
        ('username', str),
        ('phone', str),
        ('password', str),
        ('pincode', int),
        ('service_id', int),
        ('service_price', int),
    ], )
    
    # Check if email or username exists
    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        raise Conflict("email or username already in use")
    
    if not Service.query.get(service_id):
        raise NotFound(f"Service with service_id {service_id} not found.")

    filename = profile_image

    new_user = User(name=name, email=email, username=username, phone=phone,
                    address=address, pincode=pincode, latitude=latitude, about=about,
                    longitude=longitude, profile_image=filename, role="PROFESSIONAL", password=password)
    db.session.add(new_user)
    db.session.commit()
    new_professional = Professional(
        service_id=service_id,
        service_price=service_price,
        experience=experience,
        documents=documents,
        user_id=new_user.id
                    )
    db.session.add(new_professional)
    db.session.commit()
    # Notify admins
    admins = User.query.filter_by(role=Role.ADMIN).all()
    for admin in admins:
        notification = Notification(message=f"New Professional: {new_user.name}", link=f"/admin/professional/{new_user.id}", user_id=admin.id)
        db.session.add(notification)
    db.session.commit()

    user_data = {column.name: getattr(new_user, column.name) for column in User.__table__.columns}
    professional_data = {column.name: getattr(new_professional, column.name) for column in Professional.__table__.columns}

    user_data['role'] = new_user.role.name
    user_data.pop('password')

    response_data = {
        "user": user_data,
        "professional": professional_data
    }
    return jsonify(
        {
            "success": True,
            "message": "Professional account created successfully",
            "data": response_data
        }
    ), 201

def delete_professional_controller(professional_id):

    professional = Professional.query.get(professional_id)
    if not professional:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    user = User.query.get(professional.user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=True, message="Professional deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete professional with ID {professional_id}")

def edit_professional_controller(professional_id, c_user=None):

    professional = Professional.query.get(professional_id)
    if professional is None:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    
    if c_user is not None and professional.id != c_user.professional_data.id:
        raise Forbidden
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided.")
    
    name = data.get("name")
    if not name:
        data['name'] = professional.user.name
        name = professional.user.name

    username = data.get("username")
    if not username:
        data['username'] = professional.user.username
        username = professional.user.username

    email = data.get("email")
    if not email:
        data['email'] = professional.user.email
        email = professional.user.email

    phone = data.get("phone")
    if not phone:
        data['phone'] = professional.user.phone
        phone = professional.user.phone

    about = data.get("about")
    if not about:
        data['about'] = professional.user.about
        about = professional.user.about

    service_price = data.get("service_price")
    if not service_price:
        data['service_price'] = professional.service_price
        service_price = professional.service_price

    service_id = data.get("service_id")
    if not service_id:
        data['service_id'] = professional.service_id
        service_id = professional.service_id

    experience = data.get("experience")
    if not experience:
        data['experience'] = professional.experience
        experience = professional.experience

    address = data.get("address")
    if not address:
        data['address'] = professional.user.address
        address = professional.user.address

    pincode = data.get("pincode")
    if not pincode:
        data['pincode'] = professional.user.pincode
        pincode = professional.user.pincode

    latitude = data.get("latitude")
    if not latitude:
        data['latitude'] = professional.user.latitude
        latitude = professional.user.latitude

    longitude = data.get("longitude")
    if not longitude:
        data['longitude'] = professional.user.longitude
        longitude = professional.user.longitude

    profile_image = data.get("profile_image")
    if not profile_image:
        data['profile_image'] = professional.user.profile_image
        profile_image = professional.user.profile_image

    new_password = data.get("new_password")
    current_password = data.get("current_password")

    validate_fields(data, [
        ('name', str),
        ('email', str),
        ('username', str),
        ('phone', str),
        ('pincode', int),
        ('service_id', int),
        ('service_price', int),
    ], )
    # Validate unique username/email
    if User.query.filter_by(username=username).first() and username != professional.user.username:
        raise Conflict("username already exists")

    if User.query.filter_by(email=email).first() and email != professional.user.email:
        raise Conflict("email already exists") 

    professional.user.name = name
    professional.user.username = username
    professional.user.email = email
    professional.user.phone = phone
    professional.user.about = about
    professional.service_price = service_price
    professional.experience = experience
    professional.user.address = address
    professional.user.pincode = pincode
    professional.user.latitude = latitude
    professional.user.longitude = longitude
    professional.user.profile_image = profile_image

    if new_password and current_password:
        validate_fields(data, [
            ('new_password', str),
            ('current_password', str),
        ], )
        # Check if the current password is correct
        if professional.user and professional.user.check_password(professional.user.email, current_password):
            if not professional.user.check_password(professional.user.email, new_password):
                # Update the password
                professional.user.set_password(new_password)  
                
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
        return jsonify(success=True, message="Professional updated successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating professional")

def active_professional_controller(professional_id):

    professional = Professional.query.get(professional_id)
    if professional is None:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided.")
    active = data.get("active", professional.active)
    if active not in [True, False]:
        raise BadRequest("Invalid active status. Use either 'true' or 'false ")
    if active:
        professional.active = True
        professional.user.blocked = False
    else:
        professional.active = False
        professional.user.blocked = True

    try:
        db.session.commit()
        if str(active) == "True":
            return jsonify(success=True, message="Professional is now active"), 200
        else:
            return jsonify(success=True, message="Professional is blocked"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating professional")

def block_professional_controller(professional_id):

    professional = Professional.query.get(professional_id)
    if professional is None:
        raise NotFound(f"Professional with ID {professional_id} not found.")
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided.")
    block = data.get("block", professional.user.blocked)
    professional.user.blocked = block

    try:
        db.session.commit()
        if str(block) == "True":
            return jsonify(success=True, message="Professional is now blocked"), 200
        else:
            return jsonify(success=True, message="Professional is now active"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Error updating professional")

def get_professional_profile_controller(professional_id):
    professional = Professional.query.filter_by(id=professional_id).first()

    if not professional:
        raise NotFound(f"Professional with ID {professional_id} not found.")

    user = professional.user
    

    service = Service.query.filter_by(id=professional.service_id).first()
    category = Category.query.filter_by(id=service.category_id).first()
    recent_reviews = db.session.query(Customer, Review).join(Customer, Customer.id == Review.professional_id).filter(Review.professional_id == professional_id).order_by(db.desc(Review.date_created)).limit(3).all()
    
    recent_reviews_list = [
        {
            "id": review.id,
            "professional_id": review.professional_id,
            "professional_name": professional.user.name,
            "professional_image": professional.user.profile_image,
            "service_request_id": review.service_request_id,
            "description": review.description,
            "value": review.value,
            "date_created": review.date_created.strftime("%B %d, %Y %I:%M %p"),
        }
        for professional, review in recent_reviews
    ]

    professional_service = {
            "service_id":service.id,
            "service_name":service.name,
            "service_image":service.image,
            "service_price":professional.service_price,
            "service_category":category.name,
            "service_description":service.description,
    }

    profile_data = {
        "professional": {
            "id": professional_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "username": user.username,
            "about": user.about,
            "profile_image": user.profile_image,
            "documents": professional.documents,
            "address": user.address,
            "pincode": user.pincode,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "experience": professional.experience,
            "rating": professional.rating,
            "total_reviews": len(professional.reviews),
            "role": "Professional",
            "last_login": user.last_login,
            "active": professional.active,
            "blocked": user.blocked,
            "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
            "professional_service":professional_service,
            "recent_reviews":recent_reviews_list
        }
    }

    return jsonify({"success": True, "data": profile_data}), 200

def get_professional_controller(professional_id, c_user=None):
    professional = Professional.query.filter_by(id=professional_id).first()

    if not professional:
        raise NotFound(f"Professional with ID {professional_id} not found.")

    user = professional.user


    if professional and c_user is not None and c_user.professional_data.id != professional.id:
        raise Forbidden

    service = Service.query.filter_by(id=professional.service_id).first()
    category = Category.query.filter_by(id=service.category_id).first()
    recent_service_requests = ServiceRequest.query.filter_by(professional_id=professional_id).order_by(ServiceRequest.date_created.desc()).limit(3).all()
    recent_reviews = db.session.query(Customer, Review).join(Customer, Customer.id == Review.customer_id).filter(Review.professional_id == professional_id).order_by(db.desc(Review.date_created)).limit(3).all()
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
            "date_of_completion": service_request.date_of_completion.strftime("%b %d, %Y %I:%M %p") if service_request.date_of_completion else None,
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
            "professional_id": review.professional_id,
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

    professional_service = {
            "service_id":service.id,
            "service_name":service.name,
            "service_image":service.image,
            "service_price":professional.service_price,
            "service_category":category.name,
            "service_description":service.description,
    }

    profile_data = {
        "professional": {
            "id": professional_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "username": user.username,
            "about": user.about,
            "profile_image": user.profile_image,
            "documents": professional.documents,
            "address": user.address,
            "pincode": user.pincode,
            "latitude": user.latitude,
            "longitude": user.longitude,
            "experience": professional.experience,
            "rating": professional.rating,
            "total_reviews": len(professional.reviews),
            "role": "Professional",
            "last_login": user.last_login,
            "active": professional.active,
            "blocked": user.blocked,
            "date_created": user.date_created.strftime("%B %d, %Y %I:%M %p"),
            "professional_service":professional_service,
            "recent_reviews":recent_reviews_list,
            "recent_service_requests":recent_service_requests_list


        }
    }

    return jsonify({"success": True, "data": profile_data}), 200

def get_professional_summary_controller(professional_id, c_user=None):

    professional = Professional.query.filter_by(id = professional_id).first()

    if not professional:
        raise NotFound(f"Professional with ID {professional_id} not found.")

    if professional and c_user is not None and c_user.professional_data.id != professional.id:
        raise Forbidden

    review_counts = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0
    }
    total_reviews = 0
    if professional.reviews:

        for review in professional.reviews:
            rating = review.value
            total_reviews += 1
            if rating == 1:
                review_counts['1'] += 1
            elif rating == 2:
                review_counts['2'] += 1
            elif rating == 3:
                review_counts['3'] += 1
            elif rating == 4:
                review_counts['4'] += 1
            elif rating == 5:
                review_counts['5'] += 1
            
    total_service_requests = ServiceRequest.query.filter_by(professional_id=professional_id)
    current_service_requests_count = ServiceRequest.query.filter(
                                ServiceRequest.professional_id == professional_id,
                                (ServiceRequest.service_status == ServiceStatus.REQUESTED) | 
                                (ServiceRequest.service_status == ServiceStatus.ASSIGNED)
                            ).count()

    
    closed_service_requests_count = ServiceRequest.query.filter_by(professional_id=professional_id).filter_by(service_status=ServiceStatus.CLOSED).count()
    rejected_service_requests_count = ServiceRequest.query.filter_by(professional_id=professional_id).filter_by(service_status=ServiceStatus.REJECTED).count()
    assigned_service_requests_count = ServiceRequest.query.filter_by(professional_id=professional_id).filter_by(service_status=ServiceStatus.ASSIGNED).count()
    requested_service_requests_count = ServiceRequest.query.filter_by(professional_id=professional_id).filter_by(service_status=ServiceStatus.REQUESTED).count()

    revenue_data = {}
    result = []
    total_earnings = 0
    if total_service_requests:
        for service_request in total_service_requests:
            if service_request.service_status == ServiceStatus.CLOSED:
                day = service_request.date_created.strftime('%Y-%m-%d')  # e.g., "2024-01-01"
                if day not in revenue_data:
                    revenue_data[day] = 0
                revenue_data[day] += service_request.total_cost
                total_earnings += service_request.total_cost
        result = [{'day': day, 'total_revenue': total_revenue} for day, total_revenue in revenue_data.items()]

    summary_data = {
        "professional" :{
            "name": professional.user.name,
            "rating": professional.rating,
            "review_counts" : review_counts,
            "total_reviews" : total_reviews,
            "total_earnings" : total_earnings,
            "current_service_requests_count" : current_service_requests_count,
            "rejected_service_requests_count" : rejected_service_requests_count,
            "assigned_service_requests_count" : assigned_service_requests_count,
            "requested_service_requests_count" : requested_service_requests_count,
            "closed_service_requests_count" : closed_service_requests_count,
            "revenue_data" : result
        }
    }
    return jsonify({"success": True, "data": summary_data}), 200


def search_profesionals_controller():
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

    query_filter = (
            (User.name.ilike(f'%{query}%')) | 
            (User.email.ilike(f'%{query}%')) | 
            (User.username.ilike(f'%{query}%'))
    ) 
    user_results = (
        db.session.query(Professional, Service, User)
        .join(Service, Professional.service_id == Service.id)
        .join(User, Professional.user_id == User.id)
        .filter(query_filter)
    )

    # Apply the status filter only if status is provided
    if blocked == "true":
        user_results = user_results.filter(User.blocked==True)
    elif blocked == "false":
        user_results = user_results.filter(User.blocked==False)
        

    user_results = user_results.order_by(get_sorting_field(sort_by, direction))
    user_results_paginated = user_results.paginate(page=page, per_page=per_page, )

    
    users = [{'id': professional.id,
              'user_id': user.id,
              'active': professional.active,
              'blocked': user.blocked,
              'name': user.name,
              'email': user.email,
              'role': user.role.name.capitalize(),
              'date_created': user.date_created.strftime('%B %d, %Y %I:%M %p'),
              'image': user.profile_image,
              'about': user.about,
              'service_name': service.name
              
              } for professional, service, user in user_results_paginated.items]
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

