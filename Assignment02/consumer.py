import time
import logging
import click
import boto3
from widgetfactory import WidgetFactory
from widgetrequestfactory import WidgetRequestFactory
from createrequest import CreateRequest
from updaterequest import UpdateRequest
from deleterequest import DeleteRequest
from errorrequest import ErrorRequest
from
from s3puller import S3Puller
from s3pusher import S3Pusher


class Consumer:
    def __init__(self, puller, pusher, loggerName):
        self.__puller = puller
        self.__pusher = pusher
        self.__logger = logging.getLogger(loggerName)

    def consume(self, timeout=30):
        waitTime = 0
        self.__logger.info('Starting Consumer Process')
        while waitTime < timeout:
            self.__logger.info('Fetching Next Request...')
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
        widget = WidgetFactory.createWidgetFromRequest(widgetRequest)
        self.__logger.info('Widget Created Successfully')
        self.__pusher.push(widget)

    def __processUpdate(self, widgetRequest):
        self.__logger.info('Request Type: Update')
        pass

    def __processDelete(self, widgetRequest):
        self.__logger.info(f'Request Type: Delete')
        pass


@click.command()
@click.option('--rb', help='ID Of Bucket to Retrieve Widget Requests From')
@click.option('--wb', help='ID Of Bucket to Store Widgets In')
@click.option('--path', default='consumerlog.txt', help='Path to LogFile')
@click.option('-v', isflag=True, help='Verbose Mode')
def main(rb, wb, path, v):
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

    pullBucket = boto3.resource('s3').Bucket(rb)
    pushBucket = boto3.resource('s3').Bucket(wb)

    puller = S3Puller(pullBucket, loggerName)
    pusher = S3Pusher(pushBucket, loggerName)
    consumer = Consumer(puller, pusher, loggerName)
    consumer.consume()


if __name__ == "__main__":
    main()
