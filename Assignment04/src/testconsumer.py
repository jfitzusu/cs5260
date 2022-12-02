import copy
import json
import logging
import random
import time
import unittest

import producer
from widgetfactory import WidgetFactory
from widget import Widget
from widgetrequestfactory import WidgetRequestFactory
from puller import Puller
from pusher import Pusher
from widgetrequest import WidgetRequest
from createrequest import CreateRequest
from createrequest import CreateRequest
from updaterequest import UpdateRequest
from deleterequest import DeleteRequest
from errorrequest import ErrorRequest
from s3puller import S3Puller
from sqspuller import SQSPuller
from s3pusher import S3Pusher
from ddbpusher import DDBPusher
from consumer import Consumer
from consumer import main as testMain
import boto3
from sqsuploader import SQSUploader
from responder import Responder
from producer import Producer
from uploader import Uploader

TEST_REQUEST = b'{"type":"create","requestId":"74fedd3c-40ad-4df4-a759-bab394bdb1c1","widgetId":"faa894d8-109d-472c-80ca-91b04c523bc7","owner":"Henry Hops","label":"JKBI","description":"IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC","otherAttributes":[{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]}'
TEST_UPDATE = b'{"type":"update","requestId":"74fedd3c-40ad-4df4-a759-bab394bdb1c1","widgetId":"faa894d8-109d-472c-80ca-91b04c523bc7","owner":"Henry Hops","label":"JKBI","description":"notadescription","otherAttributes":[{"name":"height-unit","value":""},{"name":"vendor","value":"QEJHXIN"}]}'
TEST_DELETE = b'{"type":"delete","requestId":"74fedd3c-40ad-4df4-a759-bab394bdb1c1","widgetId":"faa894d8-109d-472c-80ca-91b04c523bc7","owner":"Henry Hops"}'
TEST_WRC = WidgetRequestFactory.fromRawJSON(TEST_REQUEST)
TEST_WRU = WidgetRequestFactory.fromRawJSON(TEST_UPDATE)
TEST_WRD = WidgetRequestFactory.fromRawJSON(TEST_DELETE)
TEST_W = WidgetFactory.widgetFromRequest(TEST_WRC)
UPDATED_W = copy.deepcopy(TEST_W)
WidgetFactory.updateWidget(UPDATED_W, TEST_WRU)
TEST_BUCKET_PULL = "usu-cs5260-snarl-test"
TEST_BUCKET_PUSH = "usu-cs5260-snarl-test"
TEST_SQS_PULL = 'TestQueue'
TEST_TABLE = 'widgets'

class ConsumerTest(unittest.TestCase):

    def testWRF(self):
        print('\n***** Unit Test 01: Test WidgetRequestFactory ************')
        widgetRequest = TEST_WRC
        assert isinstance(widgetRequest, CreateRequest)
        assert widgetRequest.getWidgetId() == "faa894d8-109d-472c-80ca-91b04c523bc7"
        assert widgetRequest.getRequestId() == "74fedd3c-40ad-4df4-a759-bab394bdb1c1"
        assert widgetRequest.getOwner() == "Henry Hops"
        assert widgetRequest.getLabel() == "JKBI"
        assert widgetRequest.getDescription() == "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC"
        assert widgetRequest.getAttributes() == [{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]

        widgetRequest.setWidgetId("34")
        assert widgetRequest.getWidgetId() == "34"

        print('Unit Test 01: Test WidgetRequestFactory: Pass')

    def testWF(self):
        print('\n***** Unit Test 02: Test WidgetFactory ************')

        widget = copy.deepcopy(TEST_W)
        assert isinstance(widget, Widget)
        assert widget.getId() == "faa894d8-109d-472c-80ca-91b04c523bc7"
        assert widget.getOwner() == "Henry Hops"
        assert widget.getLabel() == "JKBI"
        assert widget.getDescription() == "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC"
        assert widget.getAttributes() == [{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]


        WidgetFactory.updateWidget(widget, TEST_WRU)

        assert widget.getId() == "faa894d8-109d-472c-80ca-91b04c523bc7"
        assert widget.getOwner() == "Henry Hops"
        assert widget.getLabel() == "JKBI"
        assert widget.getDescription() == "notadescription"
        assert widget.getAttributes() == [{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]

        print('Unit Test 02: Test WidgetFactory: Pass')

    def testW(self):
        print('\n***** Unit Test 03: Test Widget ************')
        widget = TEST_W

        testToJson = '{"owner": "Henry Hops", "id": "faa894d8-109d-472c-80ca-91b04c523bc7", "label": "JKBI", "description": "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC", "otherAttributes": [{"name": "height-unit", "value": "cm"}, {"name": "price", "value": "47.48"}, {"name": "vendor", "value": "QEJHXIN"}]}'

        assert widget.toJson() == testToJson

        dict = widget.toDict()
        assert dict['owner'] == "Henry Hops"
        assert dict['id'] == "faa894d8-109d-472c-80ca-91b04c523bc7"
        assert dict['label'] == "JKBI"
        assert dict['description'] == "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC"
        assert dict['height-unit'] == "cm"
        assert dict['price'] == "47.48"
        assert dict['vendor'] == "QEJHXIN"

        print('Unit Test 03: Test Widget: Pass')

    # Not Quite Sure How to Get this to Work w/ Click
    # def testCLI(self):
    #     print('\n***** Unit Test 04: Test CLI ************')
    #
    #     self.assertRaises(SystemExit, testMain(rb="", wb="kk", wt="kk"))
    #     self.assertRaises(SystemExit, testMain(rb="", wb=None, wt=None))
    #
    #     print('Unit Test 04: Test CLI: Pass')

    def testPull(self):
        print('\n***** Unit Test 05: Test S3Puller ************')

        bucket = boto3.resource('s3').Bucket(TEST_BUCKET_PULL)
        randKey = random.randint(0, 1000000)
        try:
            for itemSummary in bucket.objects.all():
                item = bucket.Object(itemSummary.key)
                item.delete()

            bucket.put_object(Body=bytes('lmao', 'utf-8'), Key=str(randKey))
        except Exception:
            print('Unit Test 05: Test S3Puller: Unable to Complete')

        puller = S3Puller(bucket, 'lmao')
        item = puller.getNext()
        assert item == bytes('lmao', 'utf-8')

        print('Unit Test 05: Test S3Puller: Pass')

    def testPull2(self):
        print('\n***** Unit Test 06: Test SQSPuller ************')
        sqs = boto3.resource('sqs')
        pullQueue = sqs.get_queue_by_name(QueueName=TEST_SQS_PULL)
        try:
            pullQueue.purge()
            time.sleep(60)
            pullQueue.send_message(
                MessageBody='lmao'
            )
        except Exception:
            print(Exception)
            print('Unit Test 06: Test SQSPuller: Unable to Complete')
            self.fail()

        puller = SQSPuller(pullQueue, 'lmao')
        item = puller.getNext()
        assert item == 'lmao'
        print('Unit Test 06: Test SQSPuller: Pass')

    def testPusher(self):
        print('\n***** Unit Test 07: Test S3Pusher ************')

        bucket = boto3.resource('s3').Bucket(TEST_BUCKET_PULL)
        try:
            for itemSummary in bucket.objects.all():
                item = bucket.Object(itemSummary.key)
                item.delete()
        except Exception:
            print('Unit Test 07: Test S3Pusher: Unable to Complete')
            self.fail()

        pusher = S3Pusher(bucket, 'lmao')
        pusher.create(TEST_W)

        item = pusher.pullDown(TEST_WRU)
        print(item)
        assert item == b'{"owner": "Henry Hops", "id": "faa894d8-109d-472c-80ca-91b04c523bc7", "label": "JKBI", "description": "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC", "otherAttributes": [{"name": "height-unit", "value": "cm"}, {"name": "price", "value": "47.48"}, {"name": "vendor", "value": "QEJHXIN"}]}'

        pusher.delete(TEST_WRD)

        with self.assertRaises(Exception):
            response = bucket.Object(f"widgets/{item.getOwner()}/{item.getWidgetId()}")
            item = response.get()['Body'].read()


        print('Unit Test 07: Test S3Pusher: Pass')


    def testPusher2(self):
        print('\n***** Unit Test 08: Test DDBPusher ************')

        table = boto3.resource('dynamodb').Table(TEST_TABLE)

        pusher = DDBPusher(table, 'lmao')
        pusher.create(TEST_W)

        item = pusher.pullDown(TEST_WRU)

        assert item['owner'] == "Henry Hops"


        pusher.delete(TEST_WRD)

        with self.assertRaises(KeyError):
            item = table.get_item(Key={
                'id': TEST_W.getId()
            })['Item']

        print('Unit Test 08: Test DDBPusher: Pass')


    def testConsumer(self):
        print('\n***** Unit Test 09: Test Consumer ************')
        pusher = DummyPusher(None, None)
        puller = DummyPuller(None, None)
        logger = logging.getLogger('lmao')
        logger.setLevel(logging.CRITICAL)

        newConsumer = Consumer(puller, pusher, 'lmao')
        newConsumer.consume()

        assert pusher.result == TEST_W.toDict()
        assert pusher.newResult == UPDATED_W.toDict()
        assert pusher.garbage == TEST_W.toDict()


        print('Unit Test 09: Test Consumer: Pass')

    def testWR(self):
        print('\n***** Unit Test 10: Test Widget Request Stringify ************')
        assert TEST_WRC.toString() == TEST_REQUEST.decode('utf-8')
        assert TEST_WRD.toString() == TEST_DELETE.decode('utf-8')
        assert TEST_WRU.toString() == TEST_UPDATE.decode('utf-8')
        print('Unit Test 10: Test Widget Request Stringify: Pass')

    def testUploader(self):
        print('\n***** Unit Test 11: Test Widget Request SQSUploader ************')
        sqs = boto3.resource('sqs')
        pushQueue = sqs.get_queue_by_name(QueueName=TEST_SQS_PULL)
        pusher = SQSUploader(pushQueue, 'lmao')
        try:
            pushQueue.purge()
            time.sleep(60)
        except Exception:
            print(Exception)
            print('Unit Test 11: Test Widget Request SQSUploader: Unable to Complete')
            self.fail()

        pusher.upload(TEST_WRU)

        puller = SQSPuller(pushQueue, 'lmao')
        item = puller.getNext()
        print(item)
        print(TEST_WRU)
        assert item == TEST_WRU.toString()
        print('Unit Test 11: Test Widget Request SQSUploader: Pass')

    def testResponder(self):
        print('\n***** Unit Test 12: Test Responder ************')
        myResponder = Responder('lmao')
        response = myResponder.respond(200)
        assert "Widget Request Uploaded Successfully" in response['body']
        response = myResponder.respond(400)
        assert "ERROR: Malformed Request" in response['body']
        response = myResponder.respond(500)
        assert "ERROR: Server Error" in response['body']
        response = myResponder.respond(600)
        assert "ERROR: Unknown Error" in response['body']
        print('Unit Test 12: Test Responder: Pass')

    def testProducer(self):
        print('\n***** Unit Test 13: Test Producer ************')
        myResponder = Responder('lmao')
        myUploader = DummyUploader()
        myProducer = Producer(myResponder, myUploa der, 'lmao')
        request = '{"type":"create","requestId":"74fedd3c-40ad-4df4-a759-bab394bdb1c1","widgetId":"faa894d8-109d-472c-80ca-91b04c523bc7","owner":"Henry Hops","label":"JKBI","description":"IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC","otherAttributes":[{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]}'
        myProducer.process(request)
        print(TEST_WRC.toString())
        assert myUploader.getRequest() == request
        print('Unit Test 13: Test Producer: Pass')

    def runTest(self):
        pass





class DummyPuller(Puller):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__returned = 0

    def getNext(self):
        if self.__returned < 1:
            self.__returned += 1
            return TEST_REQUEST
        if self.__returned < 2:
            self.__returned += 1
            return TEST_UPDATE
        if self.__returned < 3:
            self.__returned += 1
            return TEST_DELETE
        return None


class DummyPusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.result = ""
        self.json = ""
        self.newResult = ""
        self.garbage = ""

    def create(self, item):
        self.result = item.toDict()
        self.json = item.toJson()

    def pullDown(self, item):
        if item.getWidgetId() == self.result['id']:
            return self.json
        else:
            return None

    def update(self, item):
        self.newResult = item.toDict()

    def delete(self, item):
        self.garbage = self.result


class DummyUploader(Uploader):
    def __init__(self):
        self.__uploaded = None

    def upload(self, request):
        self.__uploaded = request.toString()

    def getRequest(self):
        return self.__uploaded


if __name__ == '__main__':
    unittest.main()
