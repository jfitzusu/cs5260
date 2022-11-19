class WidgetAttribute:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    def getName(self):
        return self.__name

    def setName(self, newName):
        self.__name = newName

    def getValue(self):
        return self.__value

    def setValue(self, newValue):
        self.__value = newValue
