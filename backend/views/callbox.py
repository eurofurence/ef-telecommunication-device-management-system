from backend.models import CallboxTemplate, Callbox
from backend.serializers.callbox import CallboxTemplateSerializer, CallboxSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class CallboxTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows CallboxTemplates to be viewed or edited.
    """
    queryset = CallboxTemplate.objects.all()
    serializer_class = CallboxTemplateSerializer


class CallboxViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Callboxes to be viewed or edited.
    """
    queryset = Callbox.objects.all()
    serializer_class = CallboxSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_fields += [
            'extension',
            'network',
            'ip_address',
            'mac_address',
            'location',
            'has_camera',
            'camera_ip_address',
            'camera_mac_address'
        ]
