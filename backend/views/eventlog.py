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
    serializer_class = EventLogEntrySerializer
    permission_classes = [permissions.DjangoModelPermissions]
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