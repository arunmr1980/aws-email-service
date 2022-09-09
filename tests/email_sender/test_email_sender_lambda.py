import unittest
import json

import functions.email_sender.app.email_sender_lambda as email_sender

class EmailSenderLambdaTest(unittest.TestCase):

    """Successful email sending with attachment"""
    def test_email_sender_success_with_attachment(self):
        sender_event = self.get_success_event_with_attachment()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=3, exp_fail_count=0)

    
    """Successful email sending with attachment with client - Attachment bucket shared"""
    def test_email_sender_success_with_attachment_client(self):
        sender_event = self.get_success_event_with_attachment_client()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=3, exp_fail_count=0)


    """Successful email sending with attachment with client - Attachment bucket owned"""
    def test_email_sender_success_with_attachment_client_owned_bucket(self):
        sender_event = self.get_success_event_with_attachment_client_owned_bucket()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=3, exp_fail_count=0)

 
    """Successful email sending with attachment with client - Attachment bucket owned, files in root"""
    def test_email_sender_success_with_attachment_client_owned_bucket_no_folder(self):
        sender_event = self.get_success_event_with_attachment_client_owned_bucket_no_folder()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=3, exp_fail_count=0)

 
    """Email sending with attachment file loading fail"""
    def test_email_sender_success_with_attachment_fail(self):
        sender_event = self.get_success_event_with_attachment_fail()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=0, exp_fail_count=3)


    """Successful email sending"""
    def test_email_sender_success(self):
        sender_event = self.get_success_event()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=3, exp_fail_count=0)


    def test_email_sender_fail(self):
        sender_event = self.get_failure_event()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=0, exp_fail_count=3)


    def test_email_sender_partial_fail(self):
        sender_event = self.get_partial_failure_event()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.validate_response(response, exp_success_count=2, exp_fail_count=1)


    def validate_response(self, response, exp_success_count, exp_fail_count):
        to_addresses = response['to_addresses']
        success_count = 0
        fail_count = 0
        for to_address in to_addresses:
            is_sent = to_address['is_sent']
            if is_sent:
                success_count = success_count + 1
            else:
                failures = to_address['failures']
                self.validate_failures(failures)
                fail_count = fail_count + 1
        self.assertEqual(exp_success_count, success_count)
        self.assertEqual(exp_fail_count, fail_count)


    def validate_failures(self, failures):
        self.assertTrue(len(failures) > 0)
        for failure in failures:
            self.assertTrue('code' in failure and failure['code'] is not None)
            self.assertTrue('message' in failure and failure['message'] is not None)



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


    def get_success_event_with_attachment_client_owned_bucket_no_folder(self):
        return self.get_event('events/event_email_sender_fn_attachment_client_owned_bucket_no_folder.json')


    def get_success_event_with_attachment_fail(self):
        return self.get_event('events/event_email_sender_fn_attachment_fail.json')


    def get_event(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
