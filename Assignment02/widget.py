class Widget:
    def __init__(self, id, owner, label, description, attributes=None):
        if attributes is None:
            attributes = []
        self.__id = id
        self.__owner = owner
        self.__label = label
        self.__description = description
        self.__attributes = attributes

    def getId(self):
        return self.__id

    def setId(self, newId):
        assert type(newId) == str
        self.__id = newId

    def getOwner(self):
        return self.__owner

    def setOwner(self, newOwner):
        assert type(newOwner) == str
        self.__owner = newOwner

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



