"""This module provides validation help function for api endpoints"""

import re
from flask import request

def request_body_from_schema(schema):
    """Validates the latest request against a schema parameter
    Returns:
        A string if an error has occurred
        A (JSON-like) dictionary of the body if validation has passed
    """

    data = request.get_json()

    # First, validate that the request body has all the schema properties
    for attr, value in schema.items():
        if attr not in data.keys():
            # Required field not sent
            return f"Required field '{attr}' not sent"

    for attr, value in data.items():
        if attr not in schema:
            # Invalid field sent
            return f"Invalid field '{attr}'"

        if schema[attr] == "string":
            if re.fullmatch(r'\w+', value) is None:
                # Invalid value sent
                return f"Invalid value '{value}' for field '{attr}'"

    return data
