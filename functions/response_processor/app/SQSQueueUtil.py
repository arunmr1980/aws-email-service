import boto3
import uuid
from . import ESLogger as eslogger

sqs = boto3.resource('sqs')

def send_to_queue(queue_name, request):
    eslogger.info('Sending message to queue ' + queue_name)
    msgGroupId = str(uuid.uuid4())
    msgDedupId = str(uuid.uuid4())
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=request,MessageGroupId=msgGroupId, MessageDeduplicationId=msgDedupId)

