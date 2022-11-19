import logging

class Responder:
    def __init__(self, logger):
        self.__logger = logging.getLogger(logger)

    def respond(self, code):
        pass