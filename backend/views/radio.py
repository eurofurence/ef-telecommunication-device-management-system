from backend.models import RadioDevice, RadioDeviceTemplate, RadioAccessoryTemplate, RadioAccessory, PagerTemplate, \
    Pager
from backend.serializers.radio import RadioDeviceTemplateSerializer, RadioDeviceSerializer, \
    RadioAccessoryTemplateSerializer, RadioAccessorySerializer, PagerTemplateSerializer, PagerSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class RadioDeviceTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows RadioDeviceTemplates to be viewed or edited.
    """
    queryset = RadioDeviceTemplate.objects.all()
    serializer_class = RadioDeviceTemplateSerializer


class RadioDeviceViewSet(AbstractItemViewSet):
    """
    API endpoint that allows RadioDevices to be viewed or edited.
    """
    queryset = RadioDevice.objects.all()
    serializer_class = RadioDeviceSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_fields += [
            'callsign'
        ]


class RadioAccessoryTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows RadioAccessoryTemplates to be viewed or edited.
    """
    queryset = RadioAccessoryTemplate.objects.all()
    serializer_class = RadioAccessoryTemplateSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_fields += [
            'allow_quickadd'
        ]


class RadioAccessoryViewSet(AbstractItemViewSet):
    """
    API endpoint that allows RadioAccessories to be viewed or edited.
    """
    queryset = RadioAccessory.objects.all()
    serializer_class = RadioAccessorySerializer


class PagerTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows PagerTemplates to be viewed or edited.
    """
    queryset = PagerTemplate.objects.all()
    serializer_class = PagerTemplateSerializer


class PagerViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Pagers to be viewed or edited.
    """
    queryset = Pager.objects.all()
    serializer_class = PagerSerializer
