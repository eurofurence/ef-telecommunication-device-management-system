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

from collections import Counter

from django.db import transaction, IntegrityError
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import ItemBinding, Item
from backend.permissions import FullDjangoModelPermissions
from backend.serializers.binding import ItemBindingSerializer
from backend.models import RadioAccessory
from backend.models import User
from backend.views.mixins import BulkDeleteMixin


class ItemBindingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    BulkDeleteMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows ItemBindings to be viewed or edited.
    """

    serializer_class = ItemBindingSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering = ['id']
    ordering_fields = [
        'id',
        'item__template__name',
        'item__template__description',
        'item__template__owner__name',
        'item__template__owner__shortname',
        'item__serialnumber',
        'user__nickname',
        'user__ef_reg_id',
        'user__ef_security_collar_id',
        'bound_by__nickname',
        'bound_by__ef_reg_id',
        'bound_by__ef_security_collar_id'
    ]
    search_fields = [
        'item__template__name',
        'item__template__description',
        'item__template__owner__name',
        '=item__template__owner__shortname',
        'item__notes',
        'item__serialnumber',
        'user__username',
        '=user__ef_reg_id',
        '=user__ef_security_collar_id',
        'bound_by__username',
        '=bound_by__ef_reg_id',
        '=bound_by__ef_security_collar_id',
    ]

    def get_queryset(self):
        if self.request.query_params.get('userid') is not None:
            return ItemBinding.objects.filter(user__pk=self.request.query_params.get('userid'))
        else:
            return ItemBinding.objects.all()

    @action(detail=False, methods=['get'], url_path="user/(?P<userid>\\d+)")
    def get_user_bindings(self, request, userid):
        """
        Returns all bindings for the given user ID.

        :param request:
        :param userid:
        :return:
        """
        bindings = ItemBinding.objects.filter(user__id=userid)
        serializer = self.get_serializer(bindings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path="item/(?P<itemid>\\d+)")
    def get_item_binding(self, request, itemid):
        """
        Returns the binding for the given item ID, if any.

        :param request:
        :param itemid:
        :return:
        """
        binding = ItemBinding.objects.filter(item__id=itemid).first()
        if binding is None:
            return Response({}, status=404)

        serializer = self.serializer_class(binding)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Creates new bindings from the given set of items and item templates.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # Sanitize and validate data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Ensure that at least one item is to be bound
        if not data['item_ids'] and not data['item_template_ids']:
            return Response("At least one item or item template must be specified.", status=400)

        # Ensure that items to be bound are available
        if Item.objects.filter(pk__in=data['item_ids'], itembinding__isnull=False).exists():
            return Response("One or more items are already bound.", status=400)

        # Ensure that at least one item for each item template binding is available
        item_tpl_requests = Counter(data['item_template_ids'])
        for tpl_id, num_requested in item_tpl_requests.items():
            num_available = RadioAccessory.objects.filter(template=tpl_id, itembinding__isnull=True).count()
            if num_requested > num_available:
                return Response(f"Not enough quickadd items of template id {tpl_id} available. Available: {num_available} Requested: {num_requested}", status=400)

        # Bind all items
        @transaction.atomic
        def create_bindings():
            created = []

            # Get user to bind items to
            target_user = User.objects.get(pk=data['user_id'])

            # Bind items by ID
            for item_id in data['item_ids']:
                binding = ItemBinding(
                    item=Item.objects.get(pk=item_id),
                    user=target_user,
                    bound_by=request.user,
                )
                binding.save()
                created.append(binding)

            # Bind quick add items
            for tpl_id in data['item_template_ids']:
                binding = ItemBinding(
                    item=RadioAccessory.objects.filter(template=tpl_id, itembinding__isnull=True).order_by('?').first(),
                    user=target_user,
                    bound_by=request.user,
                )
                binding.save()
                created.append(binding)

            return created

        try:
            bindings = create_bindings()
            created_bindings_serializer = self.get_serializer(bindings, many=True)
            return Response(created_bindings_serializer.data, status=201)
        except IntegrityError as e:
            return Response(f"At least one requested item was already bound in the meantime. Aborting ...", status=409)
