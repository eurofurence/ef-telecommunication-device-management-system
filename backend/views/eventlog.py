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
from rest_framework import mixins
from rest_framework import filters

from backend.permissions import FullDjangoModelPermissions
from backend.serializers.eventlog import EventLogEntrySerializer
from backend.models import EventLogEntry


class EventLogEntryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows EventLogEntries to be viewed.
    """
    serializer_class = EventLogEntrySerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['-id']
    search_fields = [
        'user__username',
        'data__user__pretty_name',
        'data__item__pretty_name',
        'data__pretty_name',
        'timestamp',
        'action'
    ]

    def get_queryset(self):
        queryset = EventLogEntry.objects.all()
        actions = self.request.query_params.getlist('action')
        if actions is not None and len(actions) > 0:
            queryset = queryset.filter(action__in=actions)

        return queryset