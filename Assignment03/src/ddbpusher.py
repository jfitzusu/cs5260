import logging
import time
from pusher import Pusher

MAX_TRIES = 5
class DDBPusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def create(self, widget):
        tries = 0
        while tries < MAX_TRIES:
            try:
                self.__logger.info(f"Attempting to Upload Widget to {self.__resource.name} Table...")
                self.__resource.put_item(Item=widget.toDict())
                self.__logger.info("Upload Success")
                return
            except Exception:
                tries += 1
                time.sleep(0.1)
        self.__logger.info("Upload Failed")


    def update(self, item):
        pass

    def delete(self, item):
        self.__logger.info(f"Attempting to Delete Widget {item.getWidgetId()}...")
        try:
            self.__resource.delete_item(Key={'id': item.getWidgetId()})
            self.__logger.info("Widget Deleted Successfully")
        except Exception:
            self.__logger.warning(f"Error: Widget {item.getWidgetId()} Does Not Exist")
