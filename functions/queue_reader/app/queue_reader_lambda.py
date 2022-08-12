import json
import boto3
import os

from . import ESLogger as eslogger
from botocore.exceptions import ClientError

state_machine_arn = os.getenv('EMAIL_PROCESSOR_STATE_MACHINE_ARN')

""" Handle messages from SQS"""
def handle_event(event, context):
    batchSize = len(event['Records'])
    eslogger.info("Received message Batch from SQS --------")
    eslogger.info("Batch size " + str(batchSize))

    failed_messages = []

    for record in event['Records']:
        eslogger.info("Body of Message ----" + record['messageId'])
        eslogger.info(record["body"])
        payload = record["body"]
        stepfn_response = execute_step_function(payload)
        eslogger.debug("Step function response ")
        eslogger.debug(stepfn_response)

    response = get_response(failed_messages, batchSize)
    eslogger.info("Response :- ")
    eslogger.info(response)
    return response


def execute_step_function(payload):
    client = boto3.client('stepfunctions')
    response = client.start_execution(
                    stateMachineArn=state_machine_arn,
                    input=payload
                )
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
