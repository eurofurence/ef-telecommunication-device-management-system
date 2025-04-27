"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
    ordering_fields = [
        'id',
        'name',
        'description',
        'owner__name',
        'owner__shortname',
        'private',
        'coding__name'
    ]
    search_fields = [
        'name',
        'description',
        'owner__name',
        '=owner__shortname'
    ]


class RadioDeviceViewSet(AbstractItemViewSet):
    """
    API endpoint that allows RadioDevices to be viewed or edited.
    """
    queryset = RadioDevice.objects.all()
    serializer_class = RadioDeviceSerializer
    ordering_fields = [
        'id',
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'template__radiodevicetemplate__coding__name',
        'serialnumber',
        'callsign'
    ]
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        '=template__owner__shortname',
        'template__radiodevicetemplate__coding__name',
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
    ordering_fields = [
        'id',
        'name',
        'description',
        'owner__name',
        'owner__shortname',
        'private',
        'allow_quickadd'
    ]
    search_fields = [
        'name',
        'description',
        'owner__name',
        '=owner__shortname',
        'allow_quickadd'
    ]


class RadioAccessoryViewSet(BulkCreateMixin, AbstractItemViewSet):
    """
    API endpoint that allows RadioAccessories to be viewed or edited.
    """
    queryset = RadioAccessory.objects.all()
    serializer_class = RadioAccessorySerializer
    ordering_fields = [
        'id',
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'serialnumber'
    ]
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        '=template__owner__shortname',
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
    ordering_fields = [
        'id',
        'name',
        'description',
        'owner__name',
        'owner__shortname',
        'private'
    ]
    search_fields = [
        'name',
        'description',
        'owner__name',
        '=owner__shortname'
    ]


class PagerViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Pagers to be viewed or edited.
    """
    queryset = Pager.objects.all()
    serializer_class = PagerSerializer
    ordering_fields = [
        'id',
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'serialnumber'
    ]
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        '=template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at'
    ]
