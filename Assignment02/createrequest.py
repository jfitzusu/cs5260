from widgetrequest import WidgetRequest

class CreateRequest(WidgetRequest):
    def __init__(self, requestId, widgetId, owner, label, description, attributes=None):
        super().__init__(requestId, widgetId, owner)
        self.__label = label
        self.__description = description
        self.__attributes = attributes

    def getLabel(self):
        return self.__label

    def setLabel(self, newLabel):
        assert type(newLabel) == str
        self.__label = newLabel

    def getDescription(self):
        return self.__description

    def setDescription(self, newDescription):
        assert type(newDescription) == str
        self.__description = newDescription

    def getAttributes(self):
        return self.__attributes

    def setAttributes(self, newAttributes):
        assert type(newAttributes) == list
        self.__attributes = newAttributes


