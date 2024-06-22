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

from rest_framework import views
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import User, ItemOwner, ItemBinding, RadioDevice
from backend.permissions import FullDjangoModelPermissions
from backend.serializers import UserSerializer, ItemOwnerSerializer
from backend.views.mixins import BulkDeleteMixin


class CurrentUserProfileView(views.APIView):
    """
    API endpoint that allows the current user profile to be viewed.
    """
    queryset = User.objects.all()
    permission_classes = [FullDjangoModelPermissions]

    def get(self, request):
        if request.user is None:
            return Response(status=401)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)


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
    search_fields = [
        'nickname',
        'email',
        '=ef_reg_id',
        '=ef_security_collar_id'
    ]

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
    search_fields = [
        'name',
        '=shortname'
    ]
