import json

from . import ResponseProcessor as response_processor
from . import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from Event"""
def handle_event(event, context):
    eslogger.info("Received Event --------")
    eslogger.info(event)

    responses = []
    try:
        responses = response_processor.process_response(event)
    except ClientError as e:
        eslogger.error(e)

    

    return response
