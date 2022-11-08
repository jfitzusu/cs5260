from puller import Puller
import logging


class SQSPuller(Puller):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)
        self.__cache = []

    def getNext(self):

        if len(self.__cache) == 0:
            self.__logger.info(f'Fetching Message Batch from Queue...')
            self.__cache = self.__resource.receive_messages(
                MaxNumberOfMessages=10,
                VisibilityTimeout=30,
                WaitTimeSeconds=15
            )


        if len(self.__cache ) > 0:
            try:
                self.__logger.info(f'Checking Message {self.__cache[0].message_id} is Still Valid')
                response = self.__resource.delete_messages(
                    Entries=[
                        {
                            'Id': self.__cache[0].message_id,
                            'ReceiptHandle': self.__cache[0].receipt_handle
                        }
                    ]
                )
                if response['Successful']:
                    self.__logger.info(f'Message {self.__cache[0].message_id} Still Valid, Successfully Removed from Queue')

                content = self.__cache[0].body
                self.__cache.pop(0)
                return content

            except Exception:
                self.__cache.pop(0)
                self.__logger.info('Message Check Failed')
                return None
        else:
            self.__logger.info("No Messages in Queue")
        return None
