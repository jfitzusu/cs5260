import logging

class Puller:
    def __init__(self, resource, loggerName):
        self.__resource = resource
        self.__logger = logging.getLogger(loggerName)

    def getNext(self):
        pass