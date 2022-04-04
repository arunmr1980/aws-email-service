import json

import EmailSender as email_sender
import QueueUtil as queue_util
import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Event Bridge Trigger """
def lambda_handler_sqs(event, context):

    eslogger.info("event aka message :-")
    eslogger.info(event)

    message = event

    try:
        body = message['Body']
        payload = json.loads(body)
        response = email_sender.send_email(payload)
        queue_util.delete_message(message)
    except ClientError as e:
        eslogger.info("Printing error in handler")
        eslogger.error(e)
        eslogger.info("Printing error response in handler")
        eslogger.error(e.response)

    return get_response_from_input(event)


def get_response_from_input(event):
    response = {}
    # if event is not None and 'iteration_count' in event:
    #     response = {
    #         'iteration_count': event['iteration_count'],
    #         'iteration_max_count': event['iteration_max_count']
    #     }
    return response
