from flask import jsonify, request
from sqlalchemy import asc, desc
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from app.models import db, Notification
from app.config import PaginationConfig
from app.utils.helpers import validate_fields

# Utility function for dynamic sorting
def get_sorting_field(sort_by, direction):
    valid_sort_fields = {
        "id": Notification.id,
        "date_created": Notification.date_created,
        "link": Notification.link,
        "message": Notification.message,
        "user_id": Notification.user_id,
        "is_read": Notification.is_read,
    }

    if sort_by not in valid_sort_fields:
        raise BadRequest(
            f"Invalid sort field '{sort_by}'. Valid options are: {', '.join(valid_sort_fields.keys())}."
        )
    sort_field = valid_sort_fields[sort_by]
    return asc(sort_field) if direction == "asc" else desc(sort_field)



def get_notifications_controller(c_user):
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

    query = Notification.query.order_by(
        get_sorting_field(sort_by, direction)
    ).filter(Notification.user_id==c_user.id)
    notifications_paginated = query.paginate(page=page, per_page=per_page)

    notifications_list = []
    for notification in notifications_paginated.items:
        notifications_list.append(
            {
                "id": notification.id,
                "date_created": notification.date_created,
                "link": notification.link,
                "message": notification.message,
                "user_id": notification.user_id,
                "is_read": notification.is_read,
            }
        )
    # Return successful response with metadata
    return (
        jsonify(
            {
                "success": True,
                "data": notifications_list,
                "pagination": {
                    "total": notifications_paginated.total,
                    "pages": notifications_paginated.pages,
                    "prev_num": notifications_paginated.prev_num,
                    "next_num": notifications_paginated.next_num,
                    "current_page": notifications_paginated.page,
                    "per_page": notifications_paginated.per_page,
                },
                "sort_by": sort_by,
                "direction": direction,
            }
        ),
        200,
    )



def get_notification_controller(notification_id):

    notification = Notification.query.filter_by(id=notification_id).first()

    if not Notification:
        raise NotFound(f"Notification with ID {notification_id} not found.")

    notification_detail = {
        "id": notification.id,
        "date_created": notification.date_created,
        "link": notification.link,
        "message": notification.message,
        "user_id": notification.user_id,
        "is_read": notification.is_read,
    }
    # Return successful response with contact details
    return jsonify({"success": True, "data": notification_detail}), 200



def create_notification_controller():
    data = request.get_json()
    
    message = data.get("message")
    link = data.get("link")
    user_id = data.get("user_id")

    validate_fields(data, [
        ('message', str),
        ('link', str),
        ('user_id', int),
    ])

    new_notification = Notification(message=message, link=link, user_id=user_id)
    db.session.add(new_notification)
    db.session.commit()

    notification_data = {column.name: getattr(new_notification, column.name) for column in Notification.__table__.columns}

    return (
        jsonify(
            {
                "success": True,
                "message": "Notification created successfully",
                "data": notification_data,
            }
        ),
        201,
    )



def edit_notification_controller(notification_id):
    data = request.get_json()
    notification = Notification.query.get(notification_id)
    if notification is None:
        raise NotFound(f"Notification with ID {notification_id} not found.")

    message = data.get("message")
    if not message:
        data['message'] = notification.message
        message = notification.message
    
    link = data.get("link")
    if not link:
        data['link'] = notification.link
        link = notification.link
    
    user_id = data.get("user_id")
    if not user_id:
        data['user_id'] = notification.user_id
        user_id = notification.user_id

    validate_fields(data, [
        ('message', str),
        ('link', str),
        ('user_id', int),
    ])

    notification.message = message
    notification.link = link
    notification.user_id = user_id

    db.session.commit()
    return (
        jsonify(
            {
                "success": True,
                "message": "Notification updated successfully",
            }
        ),
        200,
    )



def delete_notification_controller(notification_id):

    notification = Notification.query.get(notification_id)
    if not notification:
        raise NotFound(f"Notification with ID {notification_id} not found.")

    try:
        db.session.delete(notification)
        db.session.commit()
        return jsonify(success=True, message="Notification deleted successfully"), 200
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Couldn't delete Notification with ID {notification_id}")


def read_notification_controller(c_user, notification_id):

    if notification_id == 0:
        notifications = Notification.query.filter_by(is_read=False, user_id=c_user.id).all()
        for notification in notifications:
            notification.is_read = True
        db.session.commit()
        return jsonify(success=True, message="Notifications successfully read"), 200
    
    notification = Notification.query.get(notification_id)
    if notification is None:
        raise NotFound(f"Notification with ID {notification_id} not found.")
    if notification.user_id != c_user.id:
        raise Forbidden


    notification.is_read = True
    db.session.commit()
    return jsonify(success=True, message="Notification successfully read"), 200