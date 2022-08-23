import unittest
import json

import functions.email_sender.app.S3FileReader as file_reader

class FileReaderTest(unittest.TestCase):

    fixture_path = 'tests/email_sender/fixtures'

    def test_get_attachment_file(self):
        folder_name = 'hiddeninsight'
        file_name = 'girl1.jpg'
        file_content = file_reader.get_attachment_file_as_binary(folder_name, file_name)
        self.assertIsNotNone(file_content)
        print(file_content)
        self.write_file(file_content)

    def write_file(self,file):
        dest_file = open('/tmp/testfile.jpg','wb')
        dest_file.write(file)
        dest_file.close()

