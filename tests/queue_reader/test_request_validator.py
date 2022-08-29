
import unittest
import json

import functions.queue_reader.app.request_validator as request_validator

class RequestValidatorTest(unittest.TestCase):

    def test_request_validator(self):
        request = self.get_email_request()

        response = request_validator.validate_request(request)
        self.assertEqual(True, response['is_valid'])


    def test_request_validator_fail(self):
        request = self.get_email_request_fail()

        response = request_validator.validate_request(request)
        self.assertEqual(False, response['is_valid'])
        self.assertTrue(response['message'] is not None)


    def test_request_validator_with_attachment(self):
        request = self.get_email_request_with_attachment()

        response = request_validator.validate_request(request)
        self.assertEqual(True, response['is_valid'])


    def get_email_request_fail(self) :
        return self.get_request('events/event_email_sender_fn_validation_fail.json')
 

    def get_email_request(self) :
        return self.get_request('events/event_email_sender_fn.json')
 
    
    def get_email_request_with_attachment(self) :
        return self.get_request('events/event_email_sender_fn_attachment_client.json')
 

    def get_request(self, file_name) :
        with open( file_name, 'r') as event:
            return event.read()
