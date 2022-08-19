import boto3
import os
from . import ESLogger as eslogger

s3 = boto3.client('s3')

bucket_name = os.getenv('ATTACHMENT_S3_BUCKET') 

def get_attachment_file(file_identifier):
    eslogger.debug('loading file from S3 - ' + str(bucket_name) + str(file_identifier))
    s3_response = s3.get_object(Bucket=bucket_name, Key=file_identifier)
    return s3_response['Body']
