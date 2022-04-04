import boto3
import os
import ESLogger as eslogger


sqs = boto3.client('sqs')

queue_url = os.getenv('EMAIL_SQS_QUEUE_URL')
max_number_of_messages = os.getenv('EMAIL_MAX_NUMBER_OF_MESSAGES')


def delete_message(message):
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    eslogger.info('Received and deleted message: %s' % message['MessageId'])
