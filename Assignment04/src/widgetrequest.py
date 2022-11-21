class WidgetRequest:
    def __init__(self, requestId, widgetId, owner):
        self.__requestId = requestId
        self.__widgetId = widgetId
        self.__owner = owner

    def getRequestId(self):
        return self.__requestId

    def setRequestId(self, newId):
        self.__requestId = newId

    def getWidgetId(self):
        return self.__widgetId

    def setWidgetId(self, newId):
        self.__widgetId = newId

    def getOwner(self):
        return self.__owner

    def setOwner(self, newOwner):
        self.__owner = newOwner

    def toString(self):
        pass
