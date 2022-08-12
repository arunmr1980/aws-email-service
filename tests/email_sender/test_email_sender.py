import unittest
import json

import functions.email_sender.app.email_sender_lambda as email_sender

class EmailSenderTest(unittest.TestCase):

    def test_email_sender(self):
        sender_event = self.get_event()
        context = None

        response = email_sender.handle_event(sender_event, context)
        self.assertEqual(200, response['statusCode'])


    def get_event(self) :
        with open( 'events/event_email_sender_fn.json', 'r') as event:
            event_dict = json.load(event)
            return event_dict