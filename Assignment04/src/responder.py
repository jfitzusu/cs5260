import logging
import os
import json


class Responder:
    def __init__(self, logger):
        self.__logger = logging.getLogger(logger)

    @staticmethod
    def respond(code):
        region = os.environ.get('AWS_REGION')
        if code == 200:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Region ": region,
                    "Result": "Widget Request Uploaded Successfully"
                })
            }
        elif code == 400:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Region ": region,
                    "Result": "ERROR: Malformed Request"
                })
            }
        elif code == 500:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Region ": region,
                    "Result": "ERROR: Server Error"
                })
            }
        else:
            return {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "Region ": region,
                    "Result": "ERROR: Unknown Error"
                })
            }
