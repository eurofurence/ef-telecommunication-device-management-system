from rest_framework import viewsets
from rest_framework import filters

from backend.models import RadioDevice, RadioDeviceTemplate, RadioAccessoryTemplate, RadioAccessory, PagerTemplate, \
    Pager, RadioCoding
from backend.permissions import FullDjangoModelPermissions
from backend.serializers.radio import RadioDeviceTemplateSerializer, RadioDeviceSerializer, \
    RadioAccessoryTemplateSerializer, RadioAccessorySerializer, PagerTemplateSerializer, PagerSerializer, \
    RadioCodingSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet
from backend.views.mixins import BulkDeleteMixin, BulkCreateMixin


class RadioCodingViewSet(BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows RadioCodings to be viewed or edited.
    """
    permission_classes = [FullDjangoModelPermissions]
    queryset = RadioCoding.objects.all()
    serializer_class = RadioCodingSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'name',
        'description',
        'color'
    ]


class RadioDeviceTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows RadioDeviceTemplates to be viewed or edited.
    """
    queryset = RadioDeviceTemplate.objects.all()
    serializer_class = RadioDeviceTemplateSerializer
    search_fields = [
        'name',
        'description',
        'owner__name',
        'owner__shortname'
    ]


class RadioDeviceViewSet(AbstractItemViewSet):
    """
    API endpoint that allows RadioDevices to be viewed or edited.
    """
    queryset = RadioDevice.objects.all()
    serializer_class = RadioDeviceSerializer
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at',
        'callsign'
    ]


class RadioAccessoryTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows RadioAccessoryTemplates to be viewed or edited.
    """
    queryset = RadioAccessoryTemplate.objects.all()
    serializer_class = RadioAccessoryTemplateSerializer
    search_fields = [
        'name',
        'description',
        'owner__name',
        'owner__shortname',
        'allow_quickadd'
    ]


class RadioAccessoryViewSet(BulkCreateMixin, AbstractItemViewSet):
    """
    API endpoint that allows RadioAccessories to be viewed or edited.
    """
    queryset = RadioAccessory.objects.all()
    serializer_class = RadioAccessorySerializer
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at'
    ]


class PagerTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows PagerTemplates to be viewed or edited.
    """
    queryset = PagerTemplate.objects.all()
    serializer_class = PagerTemplateSerializer
    search_fields = [
        'name',
        'description',
        'owner__name',
        'owner__shortname'
    ]


class PagerViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Pagers to be viewed or edited.
    """
    queryset = Pager.objects.all()
    serializer_class = PagerSerializer
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at'
    ]
