from pusher import Pusher


class S3Pusher(Pusher):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)

    def create(self, widget):
        try:
            self.__logger.info(f"Attempting to Upload Widget to widgets/{widget.getOwner()}/{widget.getId()}...")
            self.__resource.put_object(body=bytes(widget.toJson(), 'utf-8'), key=f"widgets/{widget.getOwner()}/{widget.getId()}")
            self.__logger.info("Upload Success")
        except Exception:
            self.__logger.info("Upload Failed")

    def update(self, item):
        pass

    def delete(self, item):
        pass
