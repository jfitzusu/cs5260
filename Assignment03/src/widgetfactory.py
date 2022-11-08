from widget import Widget


class WidgetFactory:
    def __init__(self):
        pass

    @staticmethod
    def widgetFromRequest(request):
        return Widget(request.getWidgetId(), request.getOwner(), request.getLabel(), request.getDescription(),
                      request.getAttributes())

    @staticmethod
    def updateWidget(oldWidget, request):
        if request.getLabel() is not None:
            if request.getLabel() == '':
                oldWidget.setLablel(None)
            else:
                oldWidget.setLablel(request.getLabel())

        if request.getDescription() is not None:
            if request.getDescription() == '':
                oldWidget.setLablel(None)
            else:
                oldWidget.setLablel(request.getLabel())

        if request.getAttributes() is not None:
            newAttributes = oldWidget.getAttributes()
            for key, value in request.getAttributes():
                if value == '':
                    del newAttributes[key]
                else:
                    newAttributes[key] = value
            oldWidget.setAttributes(newAttributes)

