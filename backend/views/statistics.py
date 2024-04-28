from rest_framework import views
from rest_framework.response import Response

from backend.models import ItemBinding, Item, User, ItemTemplate
from backend.permissions import FullDjangoModelPermissions


class StatisticsView(views.APIView):
    """
    API endpoint that returns statistics about ItemBindings
    """

    permission_classes = [FullDjangoModelPermissions]
    queryset = ItemBinding.objects.all()  # Only used for permission check

    def get(self, request, *args, **kwargs):
        total_items = Item.objects.count()
        bound_items = ItemBinding.objects.count()
        unbound_items = total_items - bound_items
        total_users = User.objects.count()
        users_with_bindings = ItemBinding.count_users_with_bindings()
        users_without_bindings = total_users - users_with_bindings

        return Response({
            'users': {
                'total': total_users,
                'with_bindings': users_with_bindings,
                'without_bindings': users_without_bindings
            },
            'templates': {
                'total': ItemTemplate.objects.count()
            },
            'items': {
                'total': total_items,
                'bound': bound_items,
                'unbound': unbound_items
            }
        })
