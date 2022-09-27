
import unittest
import json

import functions.response_processor.app.ResponseProcessor as response_processor

class ResponseProcessorTest(unittest.TestCase):


    def test_is_recoverable(self):
        self.assertTrue(response_processor.is_recoverable('Throttling'))
        self.assertFalse(response_processor.is_recoverable('dghdghfgh'))


    def test_all_success_response(self):
        event = self.get_all_success_response()

        result = response_processor.analyze_response(event)
        self.assertEqual(0, result['recoverable_failures_count'])
        self.assertEqual(0, result['non_recoverable_failures_count'])
        self.assertEqual(0, result['retry_attempts_count'])

        status = response_processor.get_response_status(event)
        self.assertEqual('SUCCESS', status)


    def test_failure_response(self):
        event = self.get_failure_response()

        result = response_processor.analyze_response(event)
        self.assertEqual(0, result['recoverable_failures_count'])
        self.assertEqual(1, result['non_recoverable_failures_count'])
        self.assertEqual(1, result['retry_attempts_count'])
        
        status = response_processor.get_response_status(event)
        self.assertEqual('FAILURE_PERMANENT', status)


    def test_recoverable_failure_response(self):
        event = self.get_recoverable_failure_response()

        result = response_processor.analyze_response(event)
        self.assertEqual(1, result['recoverable_failures_count'])
        self.assertEqual(0, result['non_recoverable_failures_count'])
        self.assertEqual(1, result['retry_attempts_count'])
        
        status = response_processor.get_response_status(event)
        self.assertEqual('FAILURE_RECOVERABLE', status)


    def test_mixed_failure_response(self):
        event = self.get_mixed_failure_response()

        result = response_processor.analyze_response(event)
        self.assertEqual(1, result['recoverable_failures_count'])
        self.assertEqual(2, result['non_recoverable_failures_count'])
        self.assertEqual(2, result['retry_attempts_count'])
        
        status = response_processor.get_response_status(event)
        self.assertEqual('FAILURE_RECOVERABLE', status)

    
    def test_retry_exceeded_failure_response(self):
        event = self.get_retry_exceeded_failure_response()

        result = response_processor.analyze_response(event)
        self.assertEqual(1, result['recoverable_failures_count'])
        self.assertEqual(2, result['non_recoverable_failures_count'])
        self.assertEqual(3, result['retry_attempts_count'])
        
        status = response_processor.get_response_status(event)
        self.assertEqual('FAILURE_PERMANENT', status)



    def get_all_success_response(self):
        return self.get_event_dict('events/response_processor.json')


    def get_failure_response(self):
        return self.get_event_dict('events/response_processor_failure.json')


    def get_recoverable_failure_response(self):
        return self.get_event_dict('events/response_processor_failure_recoverable.json')


    def get_mixed_failure_response(self):
        return self.get_event_dict('events/response_processor_failure_mixed.json')

    
    def get_retry_exceeded_failure_response(self):
        return self.get_event_dict('events/response_processor_failure_retry_exceeded.json')


    def get_event_dict(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
