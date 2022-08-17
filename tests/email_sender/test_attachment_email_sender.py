import unittest
import json

import functions.email_sender.app.EmailAttachmentSender as email_sender

class EmailAttachemntSenderTest(unittest.TestCase):

    fixture_path = 'tests/email_sender/fixtures'

    def test_email_sender_success(self):
        email_request = self.get_email_request()
        attachments = self.get_attachments()

        responses = email_sender.send_email_with_attachments(email_request, attachments)
        # for response in responses:
        #     self.assertEqual(200, response['statusCode'])

    
    def get_email_request(self):
        return self.get_file_as_dict(self.fixture_path + '/email_request.json')


    def get_attachments(self):
        attachments = []
        att1 = open(self.fixture_path + '/duck.png','rb')
        attachments.append(att1)
        return attachments


    def get_file_as_dict(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict