"""This module provides validation help function for api endpoints"""

import re
from flask import request

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
        if schema[attr] == "string":
            if (not type(value) == type("")) or (re.fullmatch(r'^[\w\s]+$', value) is None):
                return f"Invalid characters for string field '{attr}': '{value}'"
        elif schema[attr] == "int":
            if not type(value) == type(1):
                return f"Invalid type for integer field '{attr}': '{value}'"
        else:
            return f"Unknown type for field '{attr}': '{schema[attr]}'"

    return data
