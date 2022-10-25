from puller import Puller
import logging


class S3Puller(Puller):
    def __init__(self, resource, loggerName):
        super().__init__(resource, loggerName)
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def getNext(self):

        for itemSummary in self.__resource.objects.all():
            try:
                self.__logger.info(f'Attempting to Read Object: {itemSummary.key}...')
                item = self.__resource.Object(itemSummary.key)
                content = item.get()['Body']
                read = content.read()
                self.__logger.info('Read Successful. Deleting Object...')
                item.delete()
                self.__logger.info('Object Deleted')
                return read

            except self.__resource.exceptions.NoSuchKey:
                self.__logger.info('Read Failed. Attempting Next Object...')
                continue

        return None
