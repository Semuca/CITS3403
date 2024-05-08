"""This module provides validation helper functions for api endpoints"""

import re
from typing import TypedDict
from flask import request

class RequestSchemaDefinition(TypedDict):
    """Defines a schema definition for a request parameter"""

    type: str
    values: list[str] | None
    required: bool | None

def validate_request_schema(schema: dict[str, str | RequestSchemaDefinition]) -> dict[str, str] | str:
    """Validates the latest request against a schema parameter
    Returns:
        An error message string if an error has occurred
        A (JSON-like) dictionary of the body if validation has passed
    """

    # Get request data depending on the request method
    if request.method == "GET":
        data = request.args.to_dict()
    else: # Post or put requests
        data = request.get_json()

    # First, validate that the request body has all the schema properties
    for attr, value in schema.items():
        if isinstance(value, dict):
            if value["required"] is False:
                continue

        # Required fields not all sent
        if attr not in data.keys():
            return f"Required field '{attr}' not sent"

    for attr, value in data.items():
        # Unexpected field sent
        if attr not in schema:
            return f"Unexpected field '{attr}' sent"

        # If the schema is an object, convert it to a string
        schema_type = schema[attr] if isinstance(schema[attr], str) else schema[attr]["type"]
        if schema_type not in validators:
            return f"Unknown type for field '{attr}': '{schema_type}'"

        # Validate and parse by data type
        result = validators[schema_type](value, schema[attr])
        if result is None:
            return f"Invalid value '{value}' for field '{attr} ({schema_type})'"

        data[attr] = result

    return data

def validate_username(value: any, _definition: RequestSchemaDefinition) -> str | None:
    """Validates a username string"""
    if not isinstance(value, str) or re.fullmatch(r'[\w-]+', value) is None:
        return None
    return value

def validate_hash(value: any, _definition: RequestSchemaDefinition) -> str | None:
    """Validates a hash string"""
    if not isinstance(value, str) or re.fullmatch(r'[\w-]+', value) is None:
        return None
    return value

def validate_text(value: any, _definition: RequestSchemaDefinition) -> str | None:
    """Validates a general text string"""
    if not isinstance(value, str) or re.fullmatch(r'^[\w\s]+$', value) is None:
        return None
    return value

def validate_int(value: any, _definition: RequestSchemaDefinition) -> int | None:
    """Validates an integer or string that represents a digit"""
    # Parse string to int if it is a digit
    if isinstance(value, str) and value.isdigit():
        return int(value)

    if not isinstance(value, int):
        return None
    return value

def validate_enum(value: any, definition: RequestSchemaDefinition) -> str | None:
    """Validates that a value is one of the enum values"""

    # Check if the value is in one of the enum values
    for i in definition.get('values'):
        if i == value:
            return value

    return None

validators = {
    "username": validate_username,
    "hash": validate_hash,
    "text": validate_text,
    "int": validate_int,
    "enum": validate_enum,
}
