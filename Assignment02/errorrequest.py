from widgetrequest import WidgetRequest

class ErrorRequest(WidgetRequest):
    def __init__(self, error):
        super().__init__(None, None, None)
        self.__errorMessage = error

    def getMessage(self):
        return self.__errorMessage
