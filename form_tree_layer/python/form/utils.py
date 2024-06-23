import json
from json import JSONDecodeError

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

form_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 1
        },
        "description": {
            "type": "string"
        },
    },
    "required": ["name", "description"]
}

form_ids_schema = {
    "type": "object",
    "properties": {
        "form_ids": {
            "type": "array",
            "items": {
                "type": "string"
              }
        },
    },
    "required": ["form_ids"]
}


def validate_request_body(event):
    body = event.get("body")

    try:
        json_body = json.loads(body)
        validate(instance=json_body, schema=form_schema)
    except (ValidationError, JSONDecodeError):
        return False

    return True


def validate_form_ids_in_request_body(event):
    body = event.get("body")

    try:
        json_body = json.loads(body)
        validate(instance=json_body, schema=form_ids_schema)
    except (ValidationError, JSONDecodeError):
        return False

    return True


def serialize_form(item):
    serialized_item = {}

    for key in item:
        serialized_item[key] = item[key]["S"]

    return serialized_item
