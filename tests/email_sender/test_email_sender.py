import unittest
import json

import functions.email_sender.app.EmailSender as email_sender

class EmailAttachemntSenderTest(unittest.TestCase):

    fixture_path = 'tests/email_sender/fixtures'

    def test_email_sender_success(self):
        email_request = self.get_email_request()
        attachments = self.get_attachments()

        """ send_email_with_attachments method expect addresses as string array. Hence the transformation below """
        to_addresses_array = []
        for to_address in email_request['to_addresses']:
            to_addresses_array.append(to_address['email'])
        email_request['to_addresses'] = to_addresses_array

        response = email_sender.send_email_with_attachments(email_request, attachments)
        self.assertEqual(200, response['statusCode'])

    
    def test_email_sender_success_attachments_s3(self):
        email_request = self.get_email_request()

        responses = email_sender.send_email_individually(email_request)
        for response in responses:
            self.assertEqual(200, response['statusCode'])

    
    def get_email_request(self):
        return self.get_file_as_dict(self.fixture_path + '/email_request.json')


    def get_attachments(self):
        attachments = []
        file1 = open(self.fixture_path + '/duck.png','rb')
        att1 = {'name':'duck.png','file':file1.read()}
        attachments.append(att1)
        file2 = open(self.fixture_path + '/random.jpg','rb')
        att2 = {'name':'elephant.png','file':file2.read()}
        attachments.append(att2)
        return attachments


    def get_file_as_dict(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
