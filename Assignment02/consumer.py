import time
import logging
import click


@click.command()
@click.option('--rb', help='ID Of Bucket to Retrieve Widget Requests From')
@click.option('--wb', help='ID Of Bucket to Store Widgets In')
@click.option('-v', is_flag=True, help='Verbose Mode')

class Consumer():
    def __init__(self, puller, pusher):
        self.__puller = puller
        self.__pusher = pusher
        self.__logger = logging.Logger

        logging.basicConfig(filename='consumerlog.txt', filemode='w', format='[%(levelname)s] %(message)s')

    def consume(self, timeout=30):
        waitTime = 0
        while waitTime < timeout:
            nextItem = self.__puller.getNext()
            if nextItem:

                waitTime = 0
            else:
                time.sleep(0.1)
                waitTime += 0.1

    def processItem(self, item):
        widgetRequest = WidgetRequestFactory.fromRawJSON(item)

        if widgetRequest.type == "WidgetCreateRequest":
            widget = WidgetFactory.createWidgetFromRequest(widgetRequest)
            self.__pusher.push(widget)

        elif widgetRequest.type == "WidgetUpdateRequest":
            pass

        elif widgetRequest.type == "WidgetDeleteRequest":
            pass

        else:
            self.__logger.warning('Malformed Request')


if __name__ == "__main__":

