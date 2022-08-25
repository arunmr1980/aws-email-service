import unittest
import json
import os

import functions.email_sender.app.PartnerConfigUtil as config_util
from functions.email_sender.app.S3FileReader import get_file_as_binary


class PartnerConfigUtilTest(unittest.TestCase):

    bucket_name = os.getenv('ATTACHMENT_S3_BUCKET')

    def test_get_partner_configuration(self):
        partner_key = "hiddeninsight-key-9643"
        partner_config = config_util.get_partner_configuration(partner_key)
        self.assertIsNotNone(partner_config)
        self.assertEqual(partner_key, partner_config["partner_key"])

    def test_get_attachment_files_config(self):
        partner_key = "hiddeninsight-key-9643"

        """Case 1 - Only partner configuration. No clients"""
        files_config = config_util.get_attachment_files_config(partner_key, None)
        self.assertEqual("email-app-attachmentsbucket-5c4l0y3hobmw", files_config['bucket_name'])
        self.assertEqual("hiddeninsight", files_config['folder_name'])

        """Case 2 - Client share same bucket with email app"""
        files_config = config_util.get_attachment_files_config(partner_key, "mountlitera-key-1238")
        self.assertEqual("email-app-attachmentsbucket-5c4l0y3hobmw", files_config['bucket_name'])
        self.assertEqual("mountlitera", files_config['folder_name'])

        """Case 3 - Client has own bucket and folder"""
        files_config = config_util.get_attachment_files_config(partner_key, "greenchalkps-key-8528")
        self.assertEqual("ygiuhiuhiujijioji", files_config['bucket_name'])
        self.assertEqual("gcps", files_config['folder_name'])

