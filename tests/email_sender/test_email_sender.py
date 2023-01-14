import unittest
import json

import functions.email_sender.app.EmailSender as email_sender

class EmailAttachemntSenderTest(unittest.TestCase):

    fixture_path = 'tests/email_sender/fixtures'

    def test_email_sender_retry_requests(self):
        ''' All emails are tried the first time'''
        email_request = self.get_email_request_all()
        email_arr = email_sender.get_sendable_email_arr(email_request['to_addresses'])
        self.assertEqual(3, len(email_arr))

        ''' Retry after multiple failures '''
        email_request = self.get_email_retry_request()
        email_arr = email_sender.get_sendable_email_arr(email_request['to_addresses'])
        self.assertEqual(1, len(email_arr))


    def test_email_sender_success(self):
        email_request = self.get_email_request()
        attachments = self.get_attachments()

        """ send_email_with_attachments method expect addresses as string array. Hence the transformation below """
        to_addresses_array = []
        for to_address in email_request['to_addresses']:
            to_addresses_array.append(to_address['email'])
        email_request['to_addresses'] = to_addresses_array

        """ This method only returns a single response """
        response = email_sender.send_email_with_attachments(email_request, attachments)
        self.assertEqual(200, response['statusCode'])
        self.assertEqual(3, len(response['body']['emails']))

    
    def test_email_sender_success_attachments_s3(self):
        email_request = self.get_email_request()

        responses = email_sender.send_email_individually(email_request)
        for response in responses:
            self.assertEqual(200, response['statusCode'])
            self.assertEqual(1, len(response['body']['emails']))


    def get_email_request_all(self):
        return self.get_file_as_dict('events/event_email_sender_fn.json')


    def get_email_retry_request(self):
        return self.get_file_as_dict('events/response_processor_failure_mixed.json')


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
