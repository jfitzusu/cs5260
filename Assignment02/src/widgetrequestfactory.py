import json
from createrequest import CreateRequest
from updaterequest import UpdateRequest
from deleterequest import DeleteRequest
from errorrequest import ErrorRequest


class WidgetRequestFactory:
    def __init__(self):
        pass

    @staticmethod
    def fromRawJSON(rawJson):
        request = json.loads(rawJson)

        requestType = request.get('type')
        requestId = request.get('requestId')
        widgetId = request.get('widgetId')
        owner = request.get('owner')

        if not requestType or not requestId or not widgetId or not owner:
            return ErrorRequest("Malformed Request. Missing Required Fields")

        label = request.get('label')
        description = request.get('description')

        if (requestType == "create") and (not label or not description):
            return ErrorRequest("Malformed Request. Create Requests Must have a Label and Description", widgetId)

        attributes = request.get('otherAttributes')

        if requestType == "create":
            return CreateRequest(requestId, widgetId, owner, label, description, attributes)

        elif requestType == "update":
            return UpdateRequest(requestId, widgetId, owner, label, description, attributes)

        elif requestType == "delete":
            return DeleteRequest(requestId, widgetId, owner)

        else:
            return ErrorRequest("Malformed Request. Unknown Type.", widgetId)
