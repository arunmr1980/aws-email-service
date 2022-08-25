import os
import json

from . import S3FileReader as file_reader


bucket_name = os.getenv('ATTACHMENT_S3_BUCKET')

def get_partner_configuration(partner_key):
    folder_name = None
    file_name = partner_key + '.json'
    config_json = file_reader.get_file_as_text(bucket_name, folder_name, file_name)
    return json.loads(config_json)


