import time
import logging
import click
import boto3
import sys
from widgetfactory import WidgetFactory
from widgetrequestfactory import WidgetRequestFactory
from createrequest import CreateRequest
from updaterequest import UpdateRequest
from deleterequest import DeleteRequest
from errorrequest import ErrorRequest
from s3puller import S3Puller
from s3pusher import S3Pusher
from ddbpusher import DDBPusher


class Consumer:
    def __init__(self, puller, pusher, loggerName):
        self.__puller = puller
        self.__pusher = pusher
        self.__logger = logging.getLogger(loggerName)

    def consume(self, timeout=30):
        waitTime = 0
        self.__logger.info('Fetching Requests...')
        while waitTime < timeout:
            nextItem = self.__puller.getNext()
            if nextItem:

                self.__processItem(nextItem)
                waitTime = 0
            else:
                # No Log Statement Here, Would Lead to Spam
                time.sleep(0.1)
                waitTime += 0.1
        self.__logger.info('No Requests Left to Process. Shutting Down...')

    def __processItem(self, item):
        widgetRequest = WidgetRequestFactory.fromRawJSON(item)
        self.__logger.info(f'Request Found for Widget [{widgetRequest.getWidgetId()}]. Processing Request...')

        if type(widgetRequest) == CreateRequest:
            self.__processCreate(widgetRequest)

        elif type(widgetRequest) == UpdateRequest:
            self.__processUpdate(widgetRequest)

        elif type(widgetRequest) == DeleteRequest:
            self.__processDelete(widgetRequest)

        elif type(widgetRequest) == ErrorRequest:
            self.__logger.warning(widgetRequest.getMessage())

        else:
            self.__logger.error("Unable to Process Request")

    def __processCreate(self, widgetRequest):
        self.__logger.info('Request Type: Creation')
        widget = WidgetFactory.widgetFromRequest(widgetRequest)
        self.__logger.info('Widget Created Successfully')
        self.__pusher.create(widget)

    def __processUpdate(self, widgetRequest):
        # self.__logger.info('Request Type: Update')
        pass

    def __processDelete(self, widgetRequest):
        # self.__logger.info(f'Request Type: Delete')
        pass


@click.command()
@click.option('--rb', help='ID Of Bucket to Retrieve Widget Requests From')
@click.option('--wb', default=None, help='ID Of Bucket to Store Widgets In (Max 1 Storage Location Specifiable)')
@click.option('--wt', default=None, help='ID of Table to Store Widgets In (DynamoDB) (Max 1 Storage Location Specifiable)')
@click.option('--path', default='consumerlog.txt', help='Path to LogFile')
@click.option('-v', is_flag=True, help='Verbose Mode')
def main(rb, wb, wt, path, v):
    if (wb is None) and (wt is None):
        print("Error: No Write Destination Specified. Use --help to See Options")
        sys.exit(1)

    if (wb is not None) and (wt is not None):
        print("Error: Multiple Write Destinations Specified. Use --help to See Options")
        sys.exit(1)

    # The Actual Nonsense You Have to Go Through for Python Logging
    loggerName = 'consumer'
    logger = logging.getLogger(loggerName)

    cHandler = logging.StreamHandler()
    fHandler = logging.FileHandler(path)
    cHandler.setLevel(logging.INFO if v else logging.WARNING)
    fHandler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    cHandler.setFormatter(formatter)
    fHandler.setFormatter(formatter)

    logger.addHandler(cHandler)
    logger.addHandler(fHandler)
    logger.setLevel(logging.INFO)

    try:
        pullBucket = boto3.resource('s3').Bucket(rb)
        puller = S3Puller(pullBucket, loggerName)
    except Exception:
        print(f"Erro: No Such Bucket {rb}")
        sys.exit(1)

    if wb is not None:
        try:
            pushBucket = boto3.resource('s3').Bucket(wb)
            pusher = S3Pusher(pushBucket, loggerName)
        except Exception:
            print(f"ERROR: No Such Bucket {wb}")
            sys.exit(1)
    elif wt is not None:
        try:
            pushTable = boto3.resource('dynamodb').Table(wt)
            pusher = DDBPusher(pushTable, loggerName)
        except Exception:
            print(f"Error: No Such Table {wt}")
            sys.exit(1)

    consumer = Consumer(puller, pusher, loggerName)
    consumer.consume()


if __name__ == "__main__":
    main()
