from django.db import transaction
from django.db.models import ProtectedError
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


class BulkDeleteMixin:
    """
    Mixin for ViewSets that allows bulk deletion of items.
    """

    @action(detail=False, methods=['delete'], url_path="bulk/(?P<ids>[0-9,]+)")
    def bulk_delete(self, request, ids):
        """
        Deletes multiple objects at once. This operation is atomic.

        :param request: DRF API request
        :param ids: List of IDs to delete the objects for
        :return: 204 on success, 404 on error
        """
        ids_to_delete = [int(pk) for pk in ids.split(',')]

        @transaction.atomic
        def delete_objects():
            for id in ids_to_delete:
                get_object_or_404(self.get_queryset(), pk=id).delete()

        try:
            delete_objects()
        except ProtectedError as e:
            return Response(status=409, data=str(e))

        return Response(status=204)


class BulkCreateMixin:
    """
    Mixin for ViewSets that allows bulk creation of items.
    """

    @action(detail=False, methods=['post'], url_path="bulk/(?P<amount>[0-9]+)")
    def bulk_create(self, request, amount):
        """
        Creates multiple objects at once. This operation is atomic.

        :param request: DRF API request
        :param amount: Number of items to create
        :return: 201 on success, 404 on error
        """
        if int(amount) < 1 or int(amount) > 200:
            return Response(status=400, data="Amount must be between 1 and 200")

        @transaction.atomic
        def create_objects():
            objs = []
            for _ in range(int(amount)):
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                objs.append(serializer.data)

            return objs

        data = create_objects()
        return Response(data, status=201)
