from jsonschema import validate
import json
from . import ESLogger as eslogger

schema = {
            "type":"object",
            "properties": {
                "client_ref_transaction_key": {
                    "type":"string"
                },
                "transaction_key": {
                    "type":"string"
                },
                "partner_key": {
                    "type":"string"
                },
                "client_key": {
                    "type":"string"
                },
                "from": {
                    "type":"string"
                },
                "to_addresses": {
                    "type":"array",
                    "items":{
                        "type":"object",
                        "properties":{
                            "email": {
                                "type":"string",
                                "format":"email"
                            }
                        }
                    }
                },
                "title": {
                    "type":"string"
                },
                "body_html": {
                    "type":"string"
                },
                "body_text": {
                    "type":"string"
                },
                "attachments": {
                    "type": "array",
                    "items":{
                        "type":"object",
                        "properties":{
                            "name":{
                                "type": "string"
                            },
                            "file_key":{
                                "type": "string"
                            }
                        },
                        "required": ["name", "file_key"]
                    }
                }
             },
            "required": ["partner_key","from","to_addresses","title"],
            "additionalProperties": False
        }


def validate_request(request):
    is_valid = {'is_valid': True}
    try:
        request_dict = json.loads(request)
        validate(instance=request_dict, schema=schema)
    except Exception as e:
        eslogger.error(e.message)
        is_valid = {'is_valid': False, 'message': e.message}

    return is_valid
