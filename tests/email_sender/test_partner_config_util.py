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

