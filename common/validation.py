from flask import request
import re

def requestBodyFromSchema(schema):
    data = request.get_json()
    
    # First, validate that the request body has all the schema properties
    for attr, value in schema.items():
        if (attr not in data.keys()):
            # Required field not sent
            return f"Required field '{attr}' not send"
    
    for attr, value in data.items():
        if (attr not in schema):
            # Invalid field sent
            return f"Invalid field '{attr}'"
        
        if (schema[attr] == "string"):
            if (re.fullmatch(r'\w+', value) != None):
                continue
            else:    
                # Invalid value sent
                return f"Invalid value '{value}' for field '{attr}'"
    
    return data