from widget import Widget
import json


class WidgetFactory:
    def __init__(self):
        pass

    @staticmethod
    def widgetFromRequest(request):
        return Widget(request.getWidgetId(), request.getOwner(), request.getLabel(), request.getDescription(),
                      request.getAttributes())

    @staticmethod
    def widgetFromJSON(rawJson):
        if type(rawJson) == str:
            dict = json.loads(rawJson)
        else:
            dict = rawJson

        widgetId = dict.get('id')
        owner = dict.get('owner')
        label = dict.get('label')
        desc = dict.get('description')
        attrib = dict.get('otherAttributes')
        return Widget(widgetId, owner, label, desc, attrib)

    @staticmethod
    def updateWidget(oldWidget, request):
        if request.getLabel() is not None:
            if request.getLabel() == '':
                oldWidget.setLabel(None)
            else:
                oldWidget.setLabel(request.getLabel())

        if request.getDescription() is not None:
            if request.getDescription() == '':
                oldWidget.setDescription(None)
            else:
                oldWidget.setDescription(request.getDescription())

        if request.getAttributes() is not None:
            newAttributes = oldWidget.getAttributes()
            updateList = request.getAttributes()
            for item in updateList:
                for i in range(len(newAttributes)):
                    if newAttributes[i]['name'] == item['name']:
                        if item['value'] == '':
                            newAttributes.pop(i)
                            break
                        elif item['value'] is None:
                            break
                        else:
                            newAttributes[i]['value'] = item['value']
            oldWidget.setAttributes(newAttributes)

