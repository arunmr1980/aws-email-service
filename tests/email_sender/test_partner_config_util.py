import unittest
import json
import os

import functions.email_sender.app.PartnerConfigUtil as config_util
from functions.email_sender.app.S3FileReader import get_file_as_binary


class PartnerConfigUtilTest(unittest.TestCase):

    bucket_name = os.getenv('ATTACHMENT_S3_BUCKET')
    bucket_suffix = os.getenv('BUCKET_SUFFIX')

    def test_env(self):
        self.assertIsNotNone(self.bucket_name, 'env variable ATTACHMENT_S3_BUCKET is not set')
        self.assertIsNotNone(self.bucket_suffix, 'env variable BUCKET_SUFFIX is not set')


    def test_get_partner_configuration(self):
        partner_key = "hiddeninsight-key-9643"
        partner_config = config_util.get_partner_configuration(partner_key)
        self.assertIsNotNone(partner_config)
        self.assertEqual(partner_key, partner_config["partner_key"])

    """Case 1 - Only partner configuration. No clients"""
    def test_get_attachment_files_config(self):
        partner_key = "hiddeninsight-key-9643"

        files_config = config_util.get_attachment_files_config(partner_key, None)
        self.assertEqual(self.bucket_name, files_config['bucket_name'])
        self.assertEqual("hiddeninsight", files_config['folder_name'])
    

    """Case 2 - Client share same bucket with email app"""
    def test_shared_bucket_config(self):
        partner_key = "hiddeninsight-key-9643"
        files_config = config_util.get_attachment_files_config(partner_key, "mountlitera-key-1238")
        self.assertEqual(self.bucket_name, files_config['bucket_name'])
        self.assertEqual("mountlitera", files_config['folder_name'])

    
    """Case 3 - Client has own bucket and folder"""
    def test_own_bucket_client(self):
        partner_key = "hiddeninsight-key-9643"
        files_config = config_util.get_attachment_files_config(partner_key, "greenchalkps-key-8528")
        self.assertEqual("greenchalkps-emails-" + self.bucket_suffix, files_config['bucket_name'])
        self.assertEqual("gcps", files_config['folder_name'])


    """Case 4 - Client has own bucket but no folder"""
    def test_own_bucket_root_folder_client(self):
        partner_key = "hiddeninsight-key-9643"
        files_config = config_util.get_attachment_files_config(partner_key, "jackfruithouse-key-4261")
        self.assertEqual("jackfruithouse-emails-" + self.bucket_suffix, files_config['bucket_name'])
        self.assertEqual(None, files_config['folder_name'])
