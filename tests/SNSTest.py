import boto3
import os
import random
import string

SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

sns = boto3.client("sns")

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

    while index < 2:
        random_str = get_random_string()
        index = index + 1
        email_text = "{\"from\": \"arun_mr549e@protonmail.com\","
        email_text = email_text + "\"to_addresses\": [\"strider.galaxies@gmail.com\",\"merry.arun@gmail.com\"],"
        email_text = email_text + "\"title\": \"[" + str(index) + "] " + random_str + " Email Service Test\""
        email_text = email_text + ",\"body_html\": \"<p>Test 3</p>\",\"body_text\": \"Blah Blah\"}"
        send_email(email_text)


def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


test_emails()
