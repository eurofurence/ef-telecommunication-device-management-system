from backend.models import CallboxTemplate, Callbox
from backend.serializers.callbox import CallboxTemplateSerializer, CallboxSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class CallboxTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows CallboxTemplates to be viewed or edited.
    """
    queryset = CallboxTemplate.objects.all()
    serializer_class = CallboxTemplateSerializer
    search_fields = [
        'name',
        'description',
        'owner__name',
        'owner__shortname'
    ]


class CallboxViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Callboxes to be viewed or edited.
    """
    queryset = Callbox.objects.all()
    serializer_class = CallboxSerializer
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at',
        'extension',
        'network',
        'ip_address',
        'mac_address',
        'location',
        'has_camera',
        'camera_ip_address',
        'camera_mac_address'
    ]
