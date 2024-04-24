from abc import ABC

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models import RadioAccessoryTemplate, ItemCoordinates
from backend.serializers.item import ItemCoordinatesSerializer
from backend.serializers.radio import RadioAccessoryTemplateQuickAddSerializer
from backend.views.mixins import BulkDeleteMixin


class AbstractItemTemplateViewSet(ABC, BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows item templates to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']


class AbstractItemViewSet(ABC, BulkDeleteMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_items = self.filter_queryset(self.queryset.filter(itembinding__isnull=True))
        page = self.paginate_queryset(available_items)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(available_items, many=True)
        return Response(serializer.data)


class QuickAddItemTemplatesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows to list quick-add item templates.
    """
    queryset = RadioAccessoryTemplate.objects.filter(allow_quickadd=True)
    serializer_class = RadioAccessoryTemplateQuickAddSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'name',
        'description',
        'owner__name',
        'owner__shortname'
    ]


class ItemCoordinatesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows item coordinates to be viewed.
    """
    queryset = ItemCoordinates.objects.all()
    serializer_class = ItemCoordinatesSerializer
    permission_classes = [permissions.IsAuthenticated]
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
