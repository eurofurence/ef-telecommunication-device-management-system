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

from backend.models import CallboxTemplate, Callbox
from backend.serializers.callbox import CallboxTemplateSerializer, CallboxSerializer
from backend.views.item import AbstractItemTemplateViewSet, AbstractItemViewSet


class CallboxTemplateViewSet(AbstractItemTemplateViewSet):
    """
    API endpoint that allows CallboxTemplates to be viewed or edited.
    """
    queryset = CallboxTemplate.objects.all()
    serializer_class = CallboxTemplateSerializer
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


class CallboxViewSet(AbstractItemViewSet):
    """
    API endpoint that allows Callboxes to be viewed or edited.
    """
    queryset = Callbox.objects.all()
    serializer_class = CallboxSerializer
    ordering_fields = [
        'id',
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'private',
        'extension',
        'location',
        'has_camera'
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
        'location',
        'has_camera',
        'camera_network',
        'camera_ip_address',
        'camera_mac_address'
    ]
