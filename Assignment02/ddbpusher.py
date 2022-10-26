import logging

from pusher import Pusher


class DDBPusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def create(self, widget):
        try:
            self.__logger.info(f"Attempting to Upload Widget to {self.__resource.name} Table...")
            self.__resource.put_item(Item=widget.toDict())
            self.__logger.info("Upload Success")
        except Exception:
            self.__logger.info("Upload Failed")


    def update(self, item):
        pass

    def delete(self, item):
        pass
