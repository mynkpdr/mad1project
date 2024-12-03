from datetime import datetime
import pytz
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import asc, desc
from app.models import Contact, db
from app.config import PaginationConfig
from app.utils.helpers import validate_fields

def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": Contact.id,
        "name": Contact.name,
        "email": Contact.email,
        "phone": Contact.phone,
        "message": Contact.message,
        "date_created": Contact.date_created,
    }

    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)



def get_contacts_controller():
    # Get and validate query parameters for pagination
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

    query = Contact.query.order_by(get_sorting_field(sort_by, direction))
    contacts_paginated = query.paginate(page=page, per_page=per_page)

    contacts_list = []
    for contact in contacts_paginated.items:
        contacts_list.append(
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "message": contact.message,
                "date_created": contact.date_created.strftime("%B %d, %Y %I:%M %p"),
            }
        )
    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": contacts_list,
                "pagination": {
                    "total": contacts_paginated.total,
                    "pages": contacts_paginated.pages,
                    "prev_num": contacts_paginated.prev_num,
                    "next_num": contacts_paginated.next_num,
                    "current_page": contacts_paginated.page,
                    "per_page": contacts_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )



def get_contact_controller(message_id):
    # Validate the message ID
    if not message_id or not isinstance(message_id, int):
        raise BadRequest("Invalid message ID provided.")

    contact = Contact.query.filter_by(id=message_id).first()

    if not contact:
        raise NotFound(f"Contact with ID {message_id} not found.")

    contact_detail = {
        "id": contact.id,
        "name": contact.name,
        "email": contact.email,
        "phone": contact.phone,
        "message": contact.message,
        "date_created": contact.date_created.strftime("%B %d, %Y %I:%M %p"),
    }
    # Return successful response with contact details
    return jsonify({"success": True, "data": contact_detail}), 200



def delete_contact_controller(message_id):

    contact = Contact.query.get(message_id)
    if not contact:
        raise NotFound(f"Message with id {message_id} not found.")

    try:

        db.session.delete(contact)
        db.session.commit()
        return jsonify(success=True, message="Message deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception("Could not delete message.")



def create_contact_controller():
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")
    
    
    validate_fields(data, [
        ('name', str),
        ('email', str),
        ('phone', str),
        ('message', str),
    ])

    new_contact = Contact(
        name=name,
        email=email,
        phone=phone,
        message=message,
        date_created=datetime.now(pytz.timezone("Asia/Kolkata")),
    )
    db.session.add(new_contact)
    db.session.commit()

    contact_data = {column.name: getattr(new_contact, column.name) for column in Contact.__table__.columns}

    return (
        jsonify(
            {
                "success": True,
                "message": "Contact created successfully",
                "data": contact_data,
            }
        ),
        201,
    )



def search_contacts_controller():
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

    messages = Contact.query.filter(
        (Contact.name.ilike(f"%{query}%"))
        | (Contact.email.ilike(f"%{query}%"))
        | (Contact.phone.ilike(f"%{query}%"))
        | (Contact.message.ilike(f"%{query}%"))
    )

    messages_results = messages.order_by(get_sorting_field(sort_by, direction))

    message_results_paginated = messages_results.paginate(page=page, per_page=per_page)

    messages = [
        {
            "id": message.id,
            "name": message.name,
            "email": message.email,
            "phone": message.phone,
            "message": message.message,
            "date_created": message.date_created.strftime("%B %d, %Y %I:%M %p"),
        }
        for message in message_results_paginated.items
    ]
    return (
        jsonify(
            {
                "success": True,
                "data": messages,
                "pagination": {
                    "total": message_results_paginated.total,
                    "pages": message_results_paginated.pages,
                    "prev_num": message_results_paginated.prev_num,
                    "next_num": message_results_paginated.next_num,
                    "current_page": message_results_paginated.page,
                    "per_page": message_results_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )
