from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import User, ItemOwner, ItemBinding, RadioDevice
from backend.permissions import FullDjangoModelPermissions
from backend.serializers import UserSerializer, ItemOwnerSerializer
from backend.views.mixins import BulkDeleteMixin


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['nickname', 'email', 'ef_reg_id', 'ef_security_collar_id']

    @action(detail=False, methods=['get'], url_path="callsign/(?P<callsign>\\d+)")
    def by_callsign(self, request, callsign):
        """
        Return users by callsigns of devices they have currently bound.

        :param request: The API request object
        :param callsign: Callsign filter argument
        :return: API response
        """
        devices = RadioDevice.objects.filter(callsign=callsign)
        if devices:
            bindings = ItemBinding.objects.filter(item__in=devices)
            users = User.objects.filter(id__in=[binding.user.id for binding in bindings])
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(User.objects.none(), many=True)
            return Response(serializer.data)


class ItemOwnerViewSet(BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows item owners to be viewed or edited.
    """
    queryset = ItemOwner.objects.all()
    serializer_class = ItemOwnerSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'shortname']
