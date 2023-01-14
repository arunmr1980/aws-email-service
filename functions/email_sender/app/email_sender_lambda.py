import json

from . import EmailSender as email_sender
from . import ESLogger as eslogger
from botocore.exceptions import ClientError


""" Handle messages from Event"""
def handle_event(event, context):
    eslogger.info("Received Event --------")
    eslogger.info(event)

    responses = []
    try:
        responses = email_sender.send_email_individually(event)
    except ClientError as e:
        eslogger.error(e)

    eslogger.info("Email Sender Response :- ")
    eslogger.info(responses)

    response = get_response(responses, event)

    return response


def get_response(em_responses, event):
    for em_response in em_responses:
        eslogger.debug('Email Response ------')
        eslogger.debug(em_response)
        for email in em_response['body']['emails']:
            to_address = get_to_address(event, email)
            if em_response['statusCode'] == 200:
                to_address['is_sent'] = True
            else:
                to_address['is_sent'] = False
                if 'failures' not in to_address:
                    to_address['failures'] = []
                failure = {
                            'code':em_response['body']['code'],
                            'message': em_response['body']['message'],
                            'timestamp': em_response['body']['timestamp']
                        }
                to_address['failures'].append(failure)

    return event


def get_to_address(event, email):
    for to_address in event['to_addresses']:
        if to_address['email'] == email:
            return to_address

