from backend.models import PhoneTemplate, Phone
from backend.serializers.phone import PhoneTemplateSerializer, PhoneSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class PhoneTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows PhoneTemplates to be viewed or edited.
    """
    queryset = PhoneTemplate.objects.all()
    serializer_class = PhoneTemplateSerializer


class PhoneViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Phones to be viewed or edited.
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_fields += [
            'extension',
            'network',
            'ip_address',
            'mac_address',
            'location'
        ]
