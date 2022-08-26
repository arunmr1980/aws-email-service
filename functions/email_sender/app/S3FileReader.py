import boto3
from . import ESLogger as eslogger

s3 = boto3.client('s3')

def get_file_as_binary(bucket_name, folder_name, file_name):
    file_identifier = get_file_identifier(folder_name, file_name)
    eslogger.debug('loading binary file from S3 - ' + str(bucket_name) + ' :  ' + file_identifier)

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


def get_file_as_text(bucket_name, folder_name, file_name):
    file_identifier = get_file_identifier(folder_name, file_name)
    eslogger.debug('loading text file from S3 - ' + str(bucket_name) + ' :  ' + file_identifier)
    s3_response = s3.get_object(Bucket=bucket_name, Key=file_identifier)
    txt_response = s3_response['Body'].read()
    return txt_response



def get_file_identifier(folder_name, file_name):
    if file_name is None:
        raise Exception("File name can not be None")
    file_identifier = None
    if folder_name is None:
        file_identifier = file_name
    else:
        file_identifier = folder_name + '/' + file_name

    return file_identifier
