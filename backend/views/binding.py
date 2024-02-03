from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from backend.models import ItemBinding
from backend.serializers.binding import ItemBindingSerializer


class ItemBindingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ItemBindings to be viewed or edited.
    """

    serializer_class = ItemBindingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'item__template__name',
        'item__template__description',
        'item__template__owner__name',
        'item__template__owner__shortname',
        'item__notes',
        'item__serialnumber',
        'user__username',
        'user__ef_reg_id',
        'user__ef_security_collar_id',
        'bound_by__username',
        'bound_by__ef_reg_id',
        'bound_by__ef_security_collar_id',
    ]

    def get_queryset(self):
        if self.request.query_params.get('userid') is not None:
            return ItemBinding.objects.filter(user__pk=self.request.query_params.get('userid'))
        else:
            return ItemBinding.objects.all()

