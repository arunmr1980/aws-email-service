import json

from . import EmailSender as email_sender
from . import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from Event"""
def handle_event(event, context):
    eslogger.info("Received Event --------")
    eslogger.info(event)

    failed_messages = []

    try:
        response = email_sender.send_email(event)
    except ClientError as e:
        eslogger.error(e)
        failed_messages.append(event)


    response = get_response(failed_messages)
    eslogger.info("Response :- ")
    eslogger.info(response)
    return response


def get_response(failed_messages):
    response = {
        'statusCode': 200
    }
    if len(failed_messages) > 0:
        batch_items = []
        for msg in failed_messages:
            batch_items.append({"itemIdentifier": msg["messageId"]})
        response["batchItemFailures"] = batch_items
    return response
