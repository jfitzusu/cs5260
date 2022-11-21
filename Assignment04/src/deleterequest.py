from widgetrequest import WidgetRequest
import json

class DeleteRequest(WidgetRequest):
    def __init__(self, requestId, widgetId, owner):
        super().__init__(requestId, widgetId, owner)

    def toString(self):
        itemDict = {
            "type": "delete",
            "requestId": self.getRequestId(),
            "widgetId": self.getWidgetId(),
            "owner": self.getOwner(),
        }

        return json.dumps(itemDict, separators=(',', ':'))
