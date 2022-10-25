from puller import Puller
import boto3
import logging

class S3Puller(Puller):
    def __init__(self, client, source, loggerName):
        self.__client = client
        self.__source = source
        self.__logger = logging.getLogger(loggerName)
        self.__bucket = boto3.resource('s3').Bucket(source)

    def getNext(self):

        for itemSummary in self.__bucket.objects.all():
            try:
                self.__logger.info(f'Attempting to Read Object: {itemSummary.key}...')
                item = self.__bucket.Object(itemSummary.key)
                content = item.get()['Body']
                read = content.read()
                self.__logger.info('Deleting Object...')
                item.delete()
                self.__logger.info('Object Deleted...')
                return read

            except self.__client.exceptions.NoSuchKey:
                self.__logger.info('Failed To Read: Attempting Next Object')
                continue

        return None
