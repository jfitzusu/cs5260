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
        pass
