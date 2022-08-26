import unittest
import json

import functions.email_sender.app.email_sender_lambda as email_sender

class EmailSenderLambdaTest(unittest.TestCase):

    """Successful email sending with attachment"""
    def test_email_sender_success_with_attachment(self):
        sender_event = self.get_success_event_with_attachment()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(200, response['statusCode'])

    
    """Successful email sending with attachment with client - Attachment bucket shared"""
    def test_email_sender_success_with_attachment_client(self):
        sender_event = self.get_success_event_with_attachment_client()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(200, response['statusCode'])

    """Successful email sending with attachment with client - Attachment bucket owned"""
    def test_email_sender_success_with_attachment_client_owned_bucket(self):
        sender_event = self.get_success_event_with_attachment_client_owned_bucket()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(200, response['statusCode'])

 
 
    """Email sending with attachment file loading fail"""
    def test_email_sender_success_with_attachment_fail(self):
        sender_event = self.get_success_event_with_attachment_fail()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(500, response['statusCode'])


    """Successful email sending"""
    def test_email_sender_success(self):
        sender_event = self.get_success_event()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(200, response['statusCode'])


    def test_email_sender_fail(self):
        sender_event = self.get_failure_event()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        for response in responses:
            self.assertEqual(400, response['statusCode'])


    def test_email_sender_partial_fail(self):
        sender_event = self.get_partial_failure_event()
        context = None

        responses = email_sender.handle_event(sender_event, context)
        success_count = 0
        fail_count = 0
        for response in responses:
            if(response['statusCode'] == 200):
                success_count = success_count + 1
            elif (response['statusCode'] == 400):
                fail_count = fail_count + 1

        self.assertEqual(2, success_count)
        self.assertEqual(1, fail_count)


    def get_success_event(self):
        return self.get_event('events/event_email_sender_fn.json')


    def get_failure_event(self):
        return self.get_event('events/event_email_sender_fn_all_fail.json')


    def get_partial_failure_event(self):
        return self.get_event('events/event_email_sender_fn_partial_fail.json')
    

    def get_success_event_with_attachment(self):
        return self.get_event('events/event_email_sender_fn_attachment.json')
   

    def get_success_event_with_attachment_client(self):
        return self.get_event('events/event_email_sender_fn_attachment_client.json')


    def get_success_event_with_attachment_client_owned_bucket(self):
        return self.get_event('events/event_email_sender_fn_attachment_client_owned_bucket.json')


    def get_success_event_with_attachment_fail(self):
        return self.get_event('events/event_email_sender_fn_attachment_fail.json')


    def get_event(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
