from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from backend.models import PhoneTemplate, Phone
from backend.serializers.phone import PhoneTemplateSerializer, PhoneSerializer


class PhoneTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PhoneTemplates to be viewed or edited.
    """
    queryset = PhoneTemplate.objects.all()
    serializer_class = PhoneTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'description', 'owner']


class PhoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Phones to be viewed or edited.
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
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
        'location'
    ]
