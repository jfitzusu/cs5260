import time
import logging
import click



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

        if widgetRequest.type == "WidgetCreateRequest":
            self.__processCreate(widgetRequest)

        elif widgetRequest.type == "WidgetUpdateRequest":
            self.__processUpdate(widgetRequest)

        elif widgetRequest.type == "WidgetDeleteRequest":
            self.__processDelete(widgetRequest)

        else:
            self.__logger.info('Malformed Request')

    def __processCreate(self, widgetRequest):
        self.__logger.info('Request Type: Creation')
        widget = WidgetFactory.createWidgetFromRequest(widgetRequest)
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

    consumer = Consumer()
    consumer.consume()

if __name__ == "__main__":

