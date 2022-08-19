import unittest
import json

import functions.email_sender.app.S3FileReader as file_reader

class FileReaderTest(unittest.TestCase):

    fixture_path = 'tests/email_sender/fixtures'

    def test_get_attachment_file(self):
        file_identifier = 'hiddeninsight/boy4.jpg'
        file = file_reader.get_attachment_file(file_identifier)
        self.assertIsNotNone(file)
        self.write_file(file)

    def write_file(self,file):
        dest_file = open(self.fixture_path+'/testfile.jpg','wb')
        dest_file.write(file.read())
        dest_file.close()

