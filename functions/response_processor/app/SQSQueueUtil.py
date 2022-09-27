import boto3

sqs = boto3.resource('sqs')

def send_to_queue(queue_name, request):
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=request)

