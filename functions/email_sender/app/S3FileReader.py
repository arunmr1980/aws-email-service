import boto3
import os
from . import ESLogger as eslogger

s3 = boto3.client('s3')

bucket_name = os.getenv('ATTACHMENT_S3_BUCKET') 

def get_attachment_file_as_binary(folder_name, file_name):
    file_identifier = str(folder_name) + '/' + str(file_name)
    eslogger.debug('loading file from S3 - ' + str(bucket_name) + ' :  ' + file_identifier)

    with open('/tmp/'+file_name, 'wb') as output_file:
        try:
            s3.download_fileobj(bucket_name, file_identifier, output_file)
            read_file = open('/tmp/'+file_name, 'rb')
            content = read_file.read()
            read_file.close()
            return content
        except:
            eslogger.error('Error while loading file from S3')
            raise


