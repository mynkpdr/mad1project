import re
from datetime import datetime

def required_fields(fields, data):
    for field, expected_type in fields:
        if expected_type == int:
            if not data.get(field) > 0:
                raise ValueError(f"Invalid {field}")
        elif expected_type == str:
            if not len(data.get(field)) > 0:
                raise ValueError(f"Invalid {field}")
        if field == "hours_per_day":
            if not (1 <= data.get("hours_per_day") <= 24):
                raise ValueError("hours_per_day must be between 1 and 24.")
        elif field == "email":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email")):
                raise ValueError("Invalid email format")
        if field == "password":
            if not len(data.get("password")) >= 8:
                raise ValueError("password should be at least 8 characters long.")
        elif field == 'new_password':
            if not len(data.get("new_password")) >= 8:
                raise ValueError("new_password should be at least 8 characters long.")
        elif field == 'current_password':
            if not len(data.get("current_password")) >= 8:
                raise ValueError("current_password should be at least 8 characters long.")
        elif field == 'start_date':
            if datetime.fromisoformat(data.get("start_date")).date() < datetime.now().date():
                raise ValueError(f"Invalid start_date. The start_date must be greater than {datetime.now().date()}")
        elif field == 'service_status':
            if data.get("service_status").upper() not in ["REQUESTED", "ASSIGNED", "REJECTED", "CLOSED"]:
                raise ValueError(f"Invalid service_status. Valid options are 'REQUESTED','ASSIGNED', 'CLOSED', 'REJECTED'")

def validate_fields(data, fields):
    missing_fields = []
    invalid_type_fields = []

    for field, expected_type in fields:
        if field not in data:
            missing_fields.append(field)
        elif not isinstance(data.get(field), expected_type) and expected_type != datetime:
            invalid_type_fields.append((field, expected_type.__name__))
        if expected_type == datetime:
            try:
                datetime.fromisoformat(data.get(field))
            except (ValueError, TypeError):
                invalid_type_fields.append((field, "Please use ISO format (YYYY-MM-DD)."))

    if missing_fields:
        raise KeyError(f"{', '.join(missing_fields)}")
    
    if invalid_type_fields:
        invalid_details = [f"{field} (expected type: {type_})" for field, type_ in invalid_type_fields]
        raise TypeError(f"{', '.join(invalid_details)}")

    required_fields(fields, data)