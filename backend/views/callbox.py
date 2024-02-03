from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from backend.models import CallboxTemplate, Callbox
from backend.serializers.callbox import CallboxTemplateSerializer, CallboxSerializer


class CallboxTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CallboxTemplates to be viewed or edited.
    """
    queryset = CallboxTemplate.objects.all()
    serializer_class = CallboxTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'description', 'owner__name', 'owner__shortname']


class CallboxViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Callboxes to be viewed or edited.
    """
    queryset = Callbox.objects.all()
    serializer_class = CallboxSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'notes',
        'serialnumber',
        'handed_out',
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
