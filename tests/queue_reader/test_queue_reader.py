
import unittest
import json

import functions.queue_reader.app.queue_reader_lambda as queue_reader

class QueueReaderTest(unittest.TestCase):

    def test_queue_reader(self):
        event = self.get_sqs_event()
        context = None

        response = queue_reader.handle_event(event, context)
        self.assertEqual(200, response['statusCode'])
        self.assertEqual(3, response['batchSize'])


    def test_queue_reader_validation_fail(self):
        event = self.get_sqs_event_validation_fail()
        context = None

        response = queue_reader.handle_event(event, context)
        self.assertEqual(200, response['statusCode'])
        self.assertEqual(3, response['batchSize'])
        self.assertEqual(2, len(response['batchItemFailures']))


    def get_sqs_event_validation_fail(self):
        return self.get_event_dict('events/event_lambda_validation_fail.json')


    def get_sqs_event(self):
        return self.get_event_dict('events/event_lambda.json')


    def get_event_dict(self, file_name) :
        with open( file_name, 'r') as event:
            event_dict = json.load(event)
            return event_dict
