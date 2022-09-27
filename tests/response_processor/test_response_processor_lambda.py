
import unittest
import json

import functions.response_processor.app.response_processor_lambda as response_processor

class ResponseProcessorLambdaTest(unittest.TestCase):
    
    def test_all_success_response(self):
        event = self.get_all_success_response()
        result = response_processor.handle_event(event, None)


    def test_failure_response(self):
        event = self.get_failure_response()
        result = response_processor.handle_event(event, None)


    def test_recoverable_failure_response(self):
        event = self.get_recoverable_failure_response()
        result = response_processor.handle_event(event, None)


    def get_all_success_response(self):
        return self.get_event_dict('events/response_processor.json')


    def get_failure_response(self):
        return self.get_event_dict('events/response_processor_failure.json')


    def get_recoverable_failure_response(self):
        return self.get_event_dict('events/response_processor_failure_recoverable.json')


    def get_event_dict(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
