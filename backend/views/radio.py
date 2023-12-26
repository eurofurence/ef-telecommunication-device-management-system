from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from backend.models import RadioDevice, RadioDeviceTemplate, RadioAccessoryTemplate, RadioAccessory
from backend.serializers.radio import RadioDeviceTemplateSerializer, RadioDeviceSerializer, \
    RadioAccessoryTemplateSerializer, RadioAccessorySerializer


class RadioDeviceTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RadioDeviceTemplates to be viewed or edited.
    """
    queryset = RadioDeviceTemplate.objects.all()
    serializer_class = RadioDeviceTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'description', 'owner']


class RadioDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RadioDevices to be viewed or edited.
    """
    queryset = RadioDevice.objects.all()
    serializer_class = RadioDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['template__name', 'template__description', 'template__owner', 'notes', 'serialnumber', 'handed_out', 'created_at', 'updated_at', 'callsign']


class RadioAccessoryTemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RadioAccessoryTemplates to be viewed or edited.
    """
    queryset = RadioAccessoryTemplate.objects.all()
    serializer_class = RadioAccessoryTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'description', 'owner', 'allow_quickadd']


class RadioAccessoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows RadioAccessories to be viewed or edited.
    """
    queryset = RadioAccessory.objects.all()
    serializer_class = RadioAccessorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['template__name', 'template__description', 'template__owner', 'notes', 'serialnumber', 'handed_out', 'created_at', 'updated_at']