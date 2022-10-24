class WidgetRequest:
    def __init__(self, requestId, widgetId, owner, label=None, description=None, attributes=None):
        self.__requestId = requestId
        self.__widgetId = widgetId
        self.__owner = owner
        self.__label = label
        self.__description = description
        self.__attributes = attributes

    def getRequestId(self):
        return self.__requestId

    def setRequestId(self, newId):
        assert type(newId) == str
        self.__requestId = newId

    def getWidgetId(self):
        return self.__widgetId

    def setWidgetId(self, newId):
        assert type(newId) == str
        self.__widgetId = newId

    def getOwner(self):
        return self.__owner

    def setOwner(self, newOwner):
        assert type(newOwner) == str
        self.__owner = newOwner
