import logging
import boto3
from responder import Responder
from sqsuploader import SQSUploader
from widgetrequest import WidgetRequest
from widgetrequestfactory import WidgetRequestFactory
from errorrequest import ErrorRequest
import json

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
            return self.__respond(400)


        self.__logger.info(f"Request Valid. Attempting to Upload...")
        result = self.__upload(widgetRequest)
        self.__logger.info(f"Upload Result: {result}")
        return self.__respond(result)


    def __parse(self, body):
        widgetRequest = WidgetRequestFactory.fromRawJSON(body)
        return widgetRequest

    def __upload(self, request):
        return self.__uploader.upload(request)

    def __respond(self, code):
        return self.__responder.respond(code)


def produce(event, context):
    rawBody = event.get('body')
    if not isinstance(rawBody, str):
        body = json.dumps(rawBody)
    else:
        body = rawBody

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
    uploader = SQSUploader(queue, 'producer')
    processor = Producer(responder, uploader, 'producer')
    result = processor.process(body)
    return result