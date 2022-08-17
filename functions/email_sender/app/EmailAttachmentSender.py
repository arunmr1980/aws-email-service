import boto3
import json
import copy
from . import ESLogger as eslogger
from botocore.exceptions import ClientError

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


CHARSET = "UTF-8"

client = boto3.client('ses')


def send_email_with_attachments(email_dict, attachment_files):

    from_email = email_dict["from"]
    to_addresses = email_dict["to_addresses"]

    msg = MIMEMultipart('mixed')
    msg['Subject'] = email_dict["title"] 
    msg['From'] =  from_email
    msg['To'] = to_addresses[0]

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    text_body = email_dict["body_text"]
    html_body = email_dict["body_html"]
    text_part = MIMEText(text_body.encode(CHARSET), 'plain', CHARSET)
    html_part = MIMEText(html_body.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(text_part)
    msg_body.attach(html_part)

    attachment_file = attachment_files[0]
    attachment = MIMEApplication(attachment_file.read())
    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    attachment.add_header('Content-Disposition','attachment',filename='duck.png')

    msg.attach(msg_body)
    msg.attach(attachment)

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
    else:
        eslogger.info("Email sent! Message ID:"),
        eslogger.info(response['MessageId'])

