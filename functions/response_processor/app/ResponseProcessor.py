import os

from . import ESLogger as eslogger
from . import SQSQueueUtil as sqsQueueUtil


MAX_RETRY_ATTEMPTS = int(os.getenv('MAX_RETRY_COUNT'))
RECOVERABLE_ERROR_CODES = ['Throttling']

EMAIL_QUEUE_NAME = os.getenv('EMAIL_QUEUE_NAME')
DLQ_NAME = os.getenv('DLQ_NAME')


def process_response(response):
    status = get_response_status(response)
    if status == 'FAILURE_RECOVERABLE':
        eslogger.info("Failures are recoverable and max attempts not exceeded. Sending to queue for processing")
        sqsQueuUtil.send_to_queue(EMAIL_QUEUE_NAME, response)
    elif status == 'FAILURE_PERMANENT':
        eslogger.info("Can not recover from failures. Moving to DLQ")
        sqsQueuUtil.send_to_queue(DLQ_NAME, response)
    else:
        eslogger.info("All emails sent successfully")
    return response



def get_response_status(response):
    result = analyze_response(response)
    eslogger.debug('result:-')
    eslogger.debug(result)
    response_status = None

    if result['recoverable_failures_count'] == 0 and result['non_recoverable_failures_count'] == 0:
        response_status = 'SUCCESS'
    elif result['recoverable_failures_count'] > 0 and result['retry_attempts_count'] < MAX_RETRY_ATTEMPTS:
        response_status = 'FAILURE_RECOVERABLE'
    else:
        response_status = 'FAILURE_PERMANENT'
    return response_status


def mark_recoverable_failures(response):
    for to_address in response['to_addresses']:
        if 'is_sent' in to_address and to_address['is_sent'] is False:
            for failure in to_address['failures']:
                if is_recoverable(failure['code']):
                    to_address['recoverable'] = True
                else:
                    to_address['recoverable'] = False
                    '''If one failure returns a non recoverable error code, do not try again'''
                    break

    return response


def analyze_response(response):
    recoverable_failures = 0
    non_recoverable_failures = 0
    retry_attempts = 0

    mark_recoverable_failures(response)
    for to_address in response['to_addresses']:
        if 'is_sent' in to_address and to_address['is_sent'] is False:
            if 'recoverable' in to_address:
                if to_address['recoverable'] is True:
                    recoverable_failures = recoverable_failures + 1
                    eslogger.debug('++ recoverable')
                elif to_address['recoverable'] is False:
                    non_recoverable_failures = non_recoverable_failures + 1
                    eslogger.debug('++ nonrecoverable')
            #The largest failure size is set as retry attempt
            if 'failures' in to_address and len(to_address['failures']) > retry_attempts:
                retry_attempts = len(to_address['failures'])

    return {
            'recoverable_failures_count': recoverable_failures,
            'non_recoverable_failures_count': non_recoverable_failures,
            'retry_attempts_count': retry_attempts
        }


def is_recoverable(error_code):
    if error_code in RECOVERABLE_ERROR_CODES:
        return True

