import logging


class Pusher:
    def __init__(self, resource, loggerName):
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def create(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, item):
        pass
