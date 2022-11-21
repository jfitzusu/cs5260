import logging
from uploader import Uploader

class SQSUploader(Uploader):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__queue = resource
        self.__logger = logging.getLogger(loggerName)

    def upload(self, request):
        self.__logger.info(f"Attempting to Upload {request}")
        result = self.__queue.send_message(
            MessageBody=request.toString()
        )
        if result['HTTPStatusCode'] == 200:
            return 200

        return 500
