from abc import ABC

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework.response import Response


class AbstractItemTemplateViewSet(ABC, viewsets.ModelViewSet):
    """
    API endpoint that allows item templates to be viewed or edited.
    """
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


class AbstractItemViewSet(ABC, viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']
    search_fields = [
        'template__name',
        'template__description',
        'template__owner__name',
        'template__owner__shortname',
        'notes',
        'serialnumber',
        'created_at',
        'updated_at'
    ]

    @action(detail=False, methods=['get'])
    def available(self, request, pk=None):
        available_items = self.queryset.filter(itembinding__isnull=True)
        page = self.paginate_queryset(available_items)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(available_items, many=True)
        return Response(serializer.data)
