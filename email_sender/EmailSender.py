
import boto3
import json
import ESLogger as eslogger
from botocore.exceptions import ClientError


CHARSET = "UTF-8"

client = boto3.client('ses')

clientv2 = boto3.client('sesv2')

def send_email(email_dict):
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': email_dict["to_addresses"],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': email_dict["body_html"],
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': email_dict["body_text"],
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': email_dict["title"],
                },
            },
            Source=email_dict["from"]
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
        eslogger.info("Response from SES ---")
        eslogger.info(response)
    except ClientError as e:
        eslogger.error("Error from SES ----")
        eslogger.error(e.response)
        eslogger.error(e.response['Error']['Message'])
        """ Raise error so upstream services like SQS can retry """
        raise e
        # return get_error_response(e.response)
    else:
        eslogger.info("Email sent! Message ID:"),
        eslogger.info(response['MessageId'])
        return get_success_response(response)


def get_success_response(ses_response):
    response = {
        "statusCode": ses_response['ResponseMetadata']['HTTPStatusCode'],
        "body": json.dumps({
            "message": "success",
            "messageId": ses_response['MessageId']
            # "location": ip.text.replace("\n", "")
        }),
    }
    return response

def get_error_response(ses_response):
    response = {
        "statusCode": ses_response['ResponseMetadata']['HTTPStatusCode'],
        "body": json.dumps({
            "message": ses_response['Error']['Message'],
            "code": ses_response['Error']['Code'],
            "type": ses_response['Error']['Type']
        }),
    }
    return response


def add_to_suppression_list(emails):
    if emails is not None:
        for email in emails:
            response = clientv2.put_suppressed_destination(
                EmailAddress=email,
                Reason='BOUNCE'
            )
            eslogger.info('Adding ' + email + ' to suppression list')
            eslogger.info(response)
