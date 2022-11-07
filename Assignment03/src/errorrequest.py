from widgetrequest import WidgetRequest

class ErrorRequest(WidgetRequest):
    def __init__(self, error, widgetId=None):
        super().__init__(widgetId, None, None)
        self.__errorMessage = error

    def getMessage(self):
        return self.__errorMessage
