"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

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

from backend.models import PhoneTemplate, Phone
from backend.serializers.phone import PhoneTemplateSerializer, PhoneSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class PhoneTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows PhoneTemplates to be viewed or edited.
    """
    queryset = PhoneTemplate.objects.all()
    serializer_class = PhoneTemplateSerializer
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


class PhoneViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Phones to be viewed or edited.
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    ordering_fields = [
        'id',
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'private',
        'extension',
        'location'
    ]
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
