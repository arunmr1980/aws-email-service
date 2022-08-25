
import boto3
import json
import copy
from http import HTTPStatus

from . import ESLogger as eslogger
from . import S3FileReader as file_reader
from botocore.exceptions import ClientError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


CHARSET = "UTF-8"

client = boto3.client('ses')

"""Emails are sent one id at a time to avoid failure for all emails if one id is wrong"""
def send_email_individually(email_dict):
    responses = []

    has_attachment = False
    attachment_files = []
    if "attachments" in email_dict and len(email_dict["attachments"]) > 0:
        has_attachment = True
        for attachment in email_dict["attachments"]:
            folder_name = email_dict["partner_key"]
            file_name = attachment["file_key"]
            
            # Catch error condition when file could not be loaded
            try:
                attch_file_content = file_reader.get_attachment_file_as_binary(folder_name, file_name)
                attch = {
                            'name': attachment['name'],
                            'file': attch_file_content
                        }
                attachment_files.append(attch)
            except:
                eslogger.error('Attachments could not be loaded')
                response = get_internal_server_error_response({'code':'ATTCH_FAIL','message':'Attachments could not be loaded'})
                responses.append(response)
                return responses


    for to_address in email_dict["to_addresses"]:
        email_dict2 = copy.deepcopy(email_dict)
        email_dict2["to_addresses"] = [to_address['email']]
        if has_attachment:
            responses.append(send_email_with_attachments(email_dict2, attachment_files))
        else:
            responses.append(send_email(email_dict2))

    return responses


def send_email_with_attachments(email_dict, attachment_files):

    from_email = email_dict["from"]
    to_addresses = email_dict["to_addresses"]

    msg = MIMEMultipart('mixed')
    msg['Subject'] = email_dict["title"] 
    msg['From'] =  from_email
    #There is only one email as we are sending individually
    msg['To'] = to_addresses[0] 

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    text_body = email_dict["body_text"]
    html_body = email_dict["body_html"]
    text_part = MIMEText(text_body.encode(CHARSET), 'plain', CHARSET)
    html_part = MIMEText(html_body.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(text_part)
    msg_body.attach(html_part)

    msg.attach(msg_body)
    add_attachments(attachment_files,msg)

    try:
        response = client.send_raw_email(
            Source=from_email,
            Destinations=to_addresses,
            RawMessage={
                'Data':msg.as_string(),
            }
            #ConfigurationSetName=CONFIGURATION_SET
        )
    except ClientError as e:
        eslogger.error("Error from SES ----")
        eslogger.error(e.response)
        eslogger.error(e.response['Error']['Message'])
        return get_error_response(e.response)
    else:
        eslogger.info("Email sent! Message ID:"),
        eslogger.info(response['MessageId'])
        return get_success_response(response)


def add_attachments(attachment_files, message):
    for attachment_file in attachment_files:
        mime_attachment = MIMEApplication(attachment_file['file'])
        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        mime_attachment.add_header('Content-Disposition','attachment',filename=attachment_file['name'])
        message.attach(mime_attachment)


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
        return get_error_response(e.response)
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


def get_internal_server_error_response(response):
    response = {
        "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
        "body": json.dumps({
            "message": response['message'],
            "code": response['code'],
        }),
    }
    return response
