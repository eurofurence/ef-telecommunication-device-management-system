from backend.models import PhoneTemplate, Phone
from backend.serializers.phone import PhoneTemplateSerializer, PhoneSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class PhoneTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows PhoneTemplates to be viewed or edited.
    """
    queryset = PhoneTemplate.objects.all()
    serializer_class = PhoneTemplateSerializer
    search_fields = [
        'name',
        'description',
        'owner__name',
        '=owner__shortname'
    ]


class PhoneViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Phones to be viewed or edited.
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        '=template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at',
        'extension',
        'network',
        'ip_address',
        'mac_address',
        'location'
    ]
