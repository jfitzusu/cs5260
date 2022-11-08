import logging
import time
from pusher import Pusher


MAX_TRIES = 5
class S3Pusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def create(self, widget):
        tries = 0
        while tries < MAX_TRIES:
            try:
                self.__logger.info(f"Attempting to Upload Widget to widgets/{widget.getOwner().replace(' ', '-').lower()}/{widget.getId()}...")
                self.__resource.put_object(Body=bytes(widget.toJson(), 'utf-8'), Key=f"widgets/{widget.getOwner().replace(' ', '-').lower()}/{widget.getId()}")
                self.__logger.info("Upload Success")
                return
            except Exception:
                tries += 1
                time.sleep(0.1)

        self.__logger.info("Upload Failed")


    def update(self, item):
        pass

    def delete(self, item):
        self.__logger.info(f"Checking if Widget {item.getWidgetId()} Exists...")
        try:
            response = self.__resource.Object(f"widgets/{item.getOwner()}/{item.getWidgetId()}")
        except Exception:
            self.__logger.warning(f"Error: Widget {item.getWidgetId()} Does Not Exist")
            return

        try:
            response.delete()
            self.__logger.info("Widget Deleted Successfully")
        except Exception:
            self.__logger.info(f"Error: Failed to Delete Widget {item.getWidgetId()} (Reason Unknown)")

