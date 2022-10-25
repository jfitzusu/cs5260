from widgetrequest import WidgetRequest

class DeleteRequest(WidgetRequest):
    def __init__(self, requestId, widgetId, owner):
        super().__init__(requestId, widgetId, owner)
