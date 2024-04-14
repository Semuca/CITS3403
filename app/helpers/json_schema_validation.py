"""This module provides validation helper functions for api endpoints"""

import re
from flask import request

# pylint: disable=too-many-return-statements
def validate_request_schema(schema):
    """Validates the latest request against a schema parameter
    Returns:
        An error message string if an error has occurred
        A (JSON-like) dictionary of the body if validation has passed
    """

    data = request.get_json()

    # First, validate that the request body has all the schema properties
    for attr, value in schema.items():
        # Required fields not all sent
        if attr not in data.keys():
            return f"Required field '{attr}' not sent"

    for attr, value in data.items():
        # Unexpected field sent
        if attr not in schema:
            return f"Unexpected field '{attr}' sent"

        # Validate data types
        match schema[attr]:
            case "username":
                if (not isinstance(value, str)) or (re.fullmatch(r'[\w-]+', value) is None):
                    return f"Invalid value '{value}' for field '{attr}'"
            case "password":
                if (not isinstance(value, str)) or (re.fullmatch(r'[\w-]+', value) is None):
                    return f"Invalid value '{value}' for field '{attr}'"
            case "text":
                if (not isinstance(value, str)) or (re.fullmatch(r'^[\w\s]+$', value) is None):
                    return f"Invalid characters for string field '{attr}': '{value}'"
            case "int":
                if not isinstance(value, int):
                    return f"Invalid type for integer field '{attr}': '{value}'"
            case _:
                return f"Unknown type for field '{attr}': '{schema[attr]}'"

    return data
