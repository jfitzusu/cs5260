import logging
import boto3
from responder import Responder
from uploader import Uploader
from widgetrequest import WidgetRequest
from widgetrequestfactory import WidgetRequestFactory
from errorrequest import ErrorRequest

QUEUE = 'cs5260-requests'

class Producer:
    def __init__(self, responder, uploader, logger):
        self.__logger = logging.getLogger(logger)
        self.__responder = responder
        self.__uploader = uploader

    def process(self, body):
        self.__logger.info(f"Processing Request {body}")
        widgetRequest = self.__parse(body)

        if isinstance(widgetRequest, ErrorRequest):
            self.__logger.warning(f"Error: Invalid Format. Terminating")
            self.__respond(2)
            return

        self.__logger.info(f"Request Valid. Attempting to Upload...")
        result = self.__upload(widgetRequest)
        self.__logger.info(f"Upload Result: {result}")
        self.__respond(result)


    def __parse(self, body):
        widgetRequest = WidgetRequestFactory.fromRawJSON(body)
        return widgetRequest

    def __upload(self, request):
        return self.__uploader.upload(request)

    def __respond(self, code):
        self.__responder.respond(code)


def produce(body):
    loggerName = 'producer'
    logger = logging.getLogger(loggerName)

    cHandler = logging.StreamHandler()
    cHandler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    cHandler.setFormatter(formatter)

    logger.addHandler(cHandler)
    logger.setLevel(logging.INFO)

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=QUEUE)
    responder = Responder('producer')
    uploader = Uploader(queue, 'producer')
    processor = Producer(responder, uploader, 'producer')
    processor.process(body)