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

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import Order
from backend.permissions import FullDjangoModelPermissions
from backend.serializers.order import OrderSerializer


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allow Orders to be viewed or edited.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'user__username',
        '=user__ef_reg_id',
        '=user__ef_security_collar_id',
        'title',
    ]

    @action(detail=False, methods=['get'], url_path="user/(?P<userid>\\d+)")
    def get_user_orders(self, request, userid):
        """
        Returns all orders for the given user ID.

        :param request:
        :param userid:
        :return:
        """
        orders = Order.objects.filter(user__id=userid)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
