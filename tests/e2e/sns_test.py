import boto3
import os
import random
import string
import json

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

sns = boto3.client("sns")


MAIL_COUNT = 1

def send_email(email_text):

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=email_text,
        Subject="Testing Email Service from local",
        MessageGroupId=get_random_string()  ## For FIFO topic
    )
    print(response)
    print('Sending email')


def test_emails():
    index = 0

    email_request = get_sns_event()
    while index < MAIL_COUNT:
        random_str = get_random_string()
        index = index + 1
        email_request['title'] = "[" + str(index) + "]" + random_str + " Email Service Test"
        email_text = json.dumps(email_request, indent=2)
        send_email(email_text)


def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


def get_sns_event():
    return get_event('events/event_sns.json')


def get_event(file_name) :
    with open( file_name, 'r') as event:
        event_dict = json.load(event)
        return event_dict


test_emails()

