from abc import ABC

from django.db import transaction
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import Item, RadioAccessoryTemplate
from backend.serializers.radio import RadioAccessoryTemplateQuickAddSerializer


class AbstractItemTemplateViewSet(ABC, viewsets.ModelViewSet):
    """
    API endpoint that allows item templates to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = '__all__'
    ordering = ['id']


class AbstractItemViewSet(ABC, viewsets.ModelViewSet):
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

    @action(detail=False, methods=['delete'], url_path="bulk/(?P<ids>[0-9,]+)")
    def bulk_delete(self, request, ids):
        """
        Deletes multiple items at once. This operation is atomic.

        :param request:
        :param ids:
        :return:
        """
        item_ids_to_delete = [int(pk) for pk in ids.split(',')]

        @transaction.atomic
        def delete_bindings():
            for id in item_ids_to_delete:
                get_object_or_404(Item, pk=id).delete()

        delete_bindings()

        return Response(status=204)


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
