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
                WaitTimeSeconds=5
            )


        for message in self.__cache:
            # try:
                self.__logger.info(f'Checking Message {message.message_id} is Still Valid')
                response = self.__resource.delete_messages(
                    Entries=[
                        {
                            'Id': message.message_id,
                            'ReceiptHandle': message.receipt_handle
                        }
                    ]
                )
                if response['Successful']:
                    self.__logger.info(f'Message {message.message_id} Still Valid, Successfully Removed from Queue')
                content = message.body
                return content

            except Exception:
                self.__logger.info('Message Check Failed')
                return None

        return None
