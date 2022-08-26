import os
import json

from . import S3FileReader as file_reader


bucket_name = os.getenv('ATTACHMENT_S3_BUCKET')

def get_partner_configuration(partner_key):
    folder_name = None
    file_name = partner_key + '.json'
    config_json = file_reader.get_file_as_text(bucket_name, folder_name, file_name)
    return json.loads(config_json)

def get_attachment_files_config(partner_key, client_key):
    partner_config = get_partner_configuration(partner_key)
    
    bucket_name = None
    folder_name = None
    if client_key is None:
        bucket_name = partner_config['s3_bucket_name']
        folder_name = partner_config['s3_folder_name']
    else:
        for client in partner_config['clients']:
            if client['client_key'] == client_key:
                if 's3_folder_name' in client:
                    folder_name = client['s3_folder_name']
                if 's3_bucket_name' in client:
                    bucket_name = client['s3_bucket_name']
                else:
                    bucket_name = partner_config['s3_bucket_name']
                break

    return {
             "bucket_name": bucket_name,
             "folder_name": folder_name
            }
