
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


    def get_sqs_event(self) :
        with open( 'events/event_lambda.json', 'r') as event:
            event_dict = json.load(event)
            return event_dict