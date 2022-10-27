import json
import logging
import random
import unittest
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
from s3pusher import S3Pusher
from ddbpusher import DDBPusher
from consumer import Consumer
from consumer import main as testMain
import boto3

TEST_REQUEST = b'{"type":"create","requestId":"74fedd3c-40ad-4df4-a759-bab394bdb1c1","widgetId":"faa894d8-109d-472c-80ca-91b04c523bc7","owner":"Henry Hops","label":"JKBI","description":"IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC","otherAttributes":[{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]}'
TEST_WR = WidgetRequestFactory.fromRawJSON(TEST_REQUEST)
TEST_W = WidgetFactory.widgetFromRequest(TEST_WR)
TEST_BUCKET_PULL = "usu-cs5260-snarl-test"
TEST_BUCKET_PUSH = "usu-cs5260-snarl-test"
TEST_TABLE = 'widgets'

class ConsumerTest(unittest.TestCase):

    def testWRF(self):
        print('\n***** Unit Test 01: Test WidgetRequestFactory ************')
        widgetRequest = TEST_WR
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

        widget = TEST_W
        assert isinstance(widget, Widget)
        assert widget.getId() == "faa894d8-109d-472c-80ca-91b04c523bc7"
        assert widget.getOwner() == "Henry Hops"
        assert widget.getLabel() == "JKBI"
        assert widget.getDescription() == "IJFUGKKMGUSRXBEIIKPSBXHBIVFQRKEUAGHURKUZQSSEZWSJABLPPPJYTVHVUUHC"
        assert widget.getAttributes() == [{"name":"height-unit","value":"cm"},{"name":"price","value":"47.48"},{"name":"vendor","value":"QEJHXIN"}]

        widget.setOwner("lmao")
        assert widget.getOwner() == "lmao"

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
            print('Unit Test 05: Test Puller: Unable to Complete')

        puller = S3Puller(bucket, 'lmao')
        item = puller.getNext()
        assert item == bytes('lmao', 'utf-8')

        print('Unit Test 05: Test S3Puller: Pass')

    def testPush(self):
        print('\n***** Unit Test 06: Test S3Pusher ************')

        bucket = boto3.resource('s3').Bucket(TEST_BUCKET_PULL)
        try:
            for itemSummary in bucket.objects.all():
                item = bucket.Object(itemSummary.key)
                item.delete()
        except Exception:
            print('Unit Test 05: Test Puller: Unable to Complete')

        pusher = S3Pusher(bucket, 'lmao')
        pusher.create(TEST_W)

        itemSummary = list(bucket.objects.limit(1))[0]

        item = bucket.Object(itemSummary.key)
        content = item.get()['Body'].read()
        item.delete()

        assert json.loads(content)['owner'] == "Henry Hops"



        print('Unit Test 06: Test S3Pusher: Pass')


    def testPush2(self):
        print('\n***** Unit Test 07: Test DDBPusher ************')

        table = boto3.resource('dynamodb').Table(TEST_TABLE)

        pusher = DDBPusher(table, 'lmao')
        pusher.create(TEST_W)

        item = table.get_item(Key={
            'id': TEST_W.getId()
        })['Item']

        table.get_item(Key={
            'id': TEST_W.getId()
        })

        assert item['owner'] == "Henry Hops"

        print('Unit Test 07: Test DDBPusher: Pass')

    def testConsumer(self):
        print('\n***** Unit Test 08: Test Consumer ************')
        pusher = DummyPusher(None, None)
        puller = DummyPuller(None, None)
        logger = logging.getLogger('lmao')
        logger.setLevel(logging.CRITICAL)

        newConsumer = Consumer(puller, pusher, 'lmao')
        newConsumer.consume()

        assert pusher.result == TEST_W.toDict()
        print('Unit Test 08: Test Consumer: Pass')

    def runTest(self):
        pass


class DummyPuller(Puller):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__returned = False

    def getNext(self):
        if not self.__returned:
            self.__returned = True
            return TEST_REQUEST
        else:
            return None


class DummyPusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.result = ""

    def create(self, item):
        self.result = item.toDict()



if __name__ == '__main__':
    unittest.main()
