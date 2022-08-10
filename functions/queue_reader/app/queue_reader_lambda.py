import json

# import EmailSender as email_sender
from . import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from SQS"""
def handle_event(event, context):
    batchSize = len(event['Records'])
    eslogger.info("Received message Batch from SQS --------")
    eslogger.info("Batch size " + str(batchSize))

    failed_messages = []

    for record in event['Records']:
        eslogger.info("Body of Message ----" + record['messageId'])
        eslogger.info(record["body"])
        payload = json.loads(record["body"])
        # try:
        #     response = email_sender.send_email(payload)
        # except ClientError as e:
        #     failed_messages.append(record)

    response = get_response(failed_messages, batchSize)
    eslogger.info("Response :- ")
    eslogger.info(response)
    return response


""" Batch item failures are used by SQS to retry failed messages only from the batch"""
def get_response(failed_messages, batchSize):
    response = {
        'statusCode': 200,
        'batchSize': batchSize
    }
    if len(failed_messages) > 0:
        batch_items = []
        for msg in failed_messages:
            batch_items.append({"itemIdentifier": msg["messageId"]})
        response["batchItemFailures"] = batch_items
    return response
