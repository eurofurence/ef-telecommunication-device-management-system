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

from abc import ABC

from rest_framework import viewsets
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import RadioAccessoryTemplate, ItemCoordinates, Item
from backend.permissions import FullDjangoModelPermissions
from backend.serializers.item import ItemMetadataSerializer, PolymorphicItemWithCoordinatesSerializer
from backend.serializers.radio import RadioAccessoryTemplateQuickAddSerializer
from backend.views.mixins import BulkDeleteMixin


class AbstractItemTemplateViewSet(ABC, BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows item templates to be viewed or edited.
    """
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']


class AbstractItemViewSet(ABC, BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_items = self.filter_queryset(self.queryset.filter(
            itembinding__isnull=True,
            template__private=False
        ))
        page = self.paginate_queryset(available_items)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(available_items, many=True)
        return Response(serializer.data)


class ItemMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemMetadataSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'id',
        'resourcetype'
    ]


class QuickAddItemTemplatesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to list quick-add item templates.
    """
    queryset = RadioAccessoryTemplate.objects.filter(allow_quickadd=True, private=False)
    serializer_class = RadioAccessoryTemplateQuickAddSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'name',
        'description',
        'owner__name',
        '=owner__shortname'
    ]


class ItemCoordinatesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows item coordinates to be viewed.
    """
    queryset = ItemCoordinates.objects.all()
    serializer_class = PolymorphicItemWithCoordinatesSerializer
    permission_classes = [FullDjangoModelPermissions]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['id']

    @action(detail=False, methods=['get'], url_path='floor/(?P<floor>[0-9]+)')
    def by_floor(self, request, floor):
        coordinates = self.queryset.filter(floor=floor)
        page = self.paginate_queryset(coordinates)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(coordinates, many=True)
        return Response(serializer.data)
