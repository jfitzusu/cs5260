import logging

from pusher import Pusher


class S3Pusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def create(self, widget):
            self.__logger.info(f"Attempting to Upload Widget to widgets/{widget.getOwner()}/{widget.getId()}...")
            self.__resource.put_object(Body=bytes(widget.toJson(), 'utf-8'), Key=f"widgets/{widget.getOwner()}/{widget.getId()}")
            self.__logger.info("Upload Success")
        # except Exception:
        #     self.__logger.info("Upload Failed")


    def update(self, item):
        pass

    def delete(self, item):
        pass
