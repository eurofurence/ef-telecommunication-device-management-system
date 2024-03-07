from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import filters

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
    queryset = EventLogEntry.objects.all()
    serializer_class = EventLogEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'user__name',
        'user__shortname',
        'timestamp',
        'action',
    ]
