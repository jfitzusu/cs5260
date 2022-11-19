import json


class Widget:
    def __init__(self, widgetId, owner, label, description, attributes=None):
        if attributes is None:
            attributes = []
        self.__id = widgetId
        self.__owner = owner
        self.__label = label
        self.__description = description
        self.__attributes = attributes

    def getId(self):
        return self.__id

    def setId(self, newId):
        self.__id = newId

    def getOwner(self):
        return self.__owner

    def setOwner(self, newOwner):
        self.__owner = newOwner

    def getLabel(self):
        return self.__label

    def setLabel(self, newLabel):
        self.__label = newLabel

    def getDescription(self):
        return self.__description

    def setDescription(self, newDescription):
        self.__description = newDescription

    def getAttributes(self):
        return self.__attributes

    def setAttributes(self, newAttributes):
        self.__attributes = newAttributes

    def toJson(self):
        itemDict = {
            "owner": self.__owner,
            "id": self.__id,
            "label": self.__label,
            "description": self.__description,
        }

        if self.__attributes:
            itemDict['otherAttributes'] = self.__attributes

        return json.dumps(itemDict)

    def toDict(self):
        itemDict = {
            "owner": self.__owner,
            "id": self.__id,
            "label": self.__label,
            "description": self.__description,
        }

        for attribute in self.__attributes:
            itemDict[attribute['name']] = attribute['value']

        return itemDict
