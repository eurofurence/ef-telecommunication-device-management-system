from django.db import transaction
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

        delete_objects()

        return Response(status=204)
