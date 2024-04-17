from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import User, ItemOwner, ItemBinding, RadioDevice
from backend.serializers import UserSerializer, ItemOwnerSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['username', 'email', 'ef_reg_id', 'ef_security_collar_id']

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


class ItemOwnerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows item owners to be viewed or edited.
    """
    queryset = ItemOwner.objects.all()
    serializer_class = ItemOwnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = ['name', 'shortname']

    @action(detail=False, methods=['delete'], url_path="bulk/(?P<ids>[0-9,]+)")
    def bulk_delete(self, request, ids):
        """
        Deletes multiple item owners at once. This operation is atomic.

        :param request:
        :param ids:
        :return:
        """
        itemowner_ids_to_delete = [int(pk) for pk in ids.split(',')]

        @transaction.atomic
        def delete_itemowners():
            for id in itemowner_ids_to_delete:
                get_object_or_404(ItemOwner, pk=id).delete()

        delete_itemowners()

        return Response(status=204)
