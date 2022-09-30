import unittest
import json

import functions.queue_reader.app.request_util as request_util


class RequestUtilTest(unittest.TestCase):


    def test_pre_process_request(self):
        request = self.get_email_request()
        pre_processed_request = request_util.pre_process_request(request)
        pre_processed_request_dict = json.loads(pre_processed_request)
        self.assertTrue('transaction_key' in pre_processed_request_dict)


    def get_email_request(self) :
        return self.get_request('events/event_email_sender_fn.json')


    def get_request(self, file_name) :
        with open( file_name, 'r') as event:
            return event.read()

