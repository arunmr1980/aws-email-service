import boto3
import os
import ESLogger as eslogger


sqs = boto3.client('sqs')

queue_url = os.getenv('EMAIL_SQS_QUEUE_URL')
max_number_of_messages = os.getenv('EMAIL_MAX_NUMBER_OF_MESSAGES')

def get_messages():
    messages = []
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=int(max_number_of_messages),
        MessageAttributeNames=[
            'All'
        ],
        # VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if 'Messages' in response:
        messages = response['Messages']
    return messages
