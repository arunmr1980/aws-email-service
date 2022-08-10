import json

import EmailSender as email_sender
import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from SQS"""
def lambda_handler_sqs(event, context):
    eslogger.info("Received message Batch from SQS --------")
    eslogger.info("Batch size " + str(len(event['Records'])))

    failed_messages = []

    for record in event['Records']:
        eslogger.info("Body of Message ----" + record['messageId'])
        eslogger.info(record["body"])
        payload = json.loads(record["body"])
        try:
            response = email_sender.send_email(payload)
        except ClientError as e:
            failed_messages.append(record)

    response = get_response(failed_messages)
    eslogger.info("Response :- ")
    eslogger.info(response)
    return response


""" Batch item failures are used by SQS to retry failed messages only from the batch"""
def get_response(failed_messages):
    response = {}
    if len(failed_messages) > 0:
        batch_items = []
        for msg in failed_messages:
            batch_items.append({"itemIdentifier": msg["messageId"]})
        response["batchItemFailures"] = batch_items
    return response
