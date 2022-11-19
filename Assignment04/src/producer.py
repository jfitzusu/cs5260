import logging
class Producer:
    def __init__(self, responder, uploader, logger):
        self.__logger = logging.getLogger(logger)
        self.__responder = responder
        self.__uploader = uploader

    def process(self, body):
        pass

    def upload(self, request):
        pass

    def respond(self, code):
        pass