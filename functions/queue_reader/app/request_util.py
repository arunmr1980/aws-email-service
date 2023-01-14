import uuid
import json

def pre_process_request(request):
    request_dict = json.loads(request)
    if 'transaction_key' not in request_dict or len(request_dict['transaction_key'].strip()) == 0:
        request_dict['transaction_key'] = get_key()
    processed_request = json.dumps(request_dict)
    return processed_request


def get_key():
    return str(uuid.uuid4())

