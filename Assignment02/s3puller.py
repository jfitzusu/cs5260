from puller import Puller


class S3Puller(Puller):
    def __init__(self, client, source, logger):
        self.__client = client
        self.__source = source
        self.__logger = logger
        self.__bucket = client.Bucket(source)

    def getNext(self):

        for itemSummary in self.__bucket.objects.all():
            try:
                item = self.__client(itemSummary.bucket_name, itemSummary.key)
                content = item.get()['Body']
                return content.read()

                break
            except Exception:
                pass

        return None
