import time
import logging

class Consumer():
    def __init__(self, puller, pusher):
        self.__puller = puller
        self.__pusher = pusher
        self.__logger = logging.Logger

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

