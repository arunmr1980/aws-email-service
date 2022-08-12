import json

from . import EmailSender as email_sender
from . import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from SQS"""
def handle_event(event, context):
    eslogger.info("Received Event --------")
    eslogger.info(event)
    eslogger.info("Context")
    eslogger.info(context)

    failed_messages = []

    # for record in event['Records']:
    #     eslogger.info("Body of Message ----" + record['messageId'])
    #     eslogger.info(record["body"])
    #     payload = json.loads(record["body"])
    #     try:
    #         response = email_sender.send_email(payload)
    #     except ClientError as e:
    #         failed_messages.append(record)

    response = get_response(failed_messages)
    eslogger.info("Response :- ")
    eslogger.info(response)
    return response


""" Batch item failures are used by SQS to retry failed messages only from the batch"""
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
