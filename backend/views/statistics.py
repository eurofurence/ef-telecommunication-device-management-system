from django.db.models import Count
from rest_framework import views
from rest_framework.response import Response

from backend.models import ItemBinding, Item, User, ItemTemplate, RadioDeviceTemplate, RadioDevice, RadioAccessory, \
    RadioAccessoryTemplate, Pager, PagerTemplate, PhoneTemplate, Phone, CallboxTemplate, Callbox
from backend.permissions import FullDjangoModelPermissions


class StatisticsView(views.APIView):
    """
    API endpoint that returns statistics about ItemBindings
    """

    permission_classes = [FullDjangoModelPermissions]
    queryset = ItemBinding.objects.all()  # Only used for permission check

    def get(self, request, *args, **kwargs):
        total_items = Item.objects.count()
        total_private_items = 0  # FIXME
        total_bindable_items = total_items - total_private_items
        bound_items = ItemBinding.objects.count()
        unbound_items = total_bindable_items - bound_items

        total_users = User.objects.count()
        users_with_bindings = ItemBinding.count_users_with_bindings()
        users_without_bindings = total_users - users_with_bindings

        return Response({
            'users': {
                'total': total_users,
                'with_bindings': users_with_bindings,
                'without_bindings': users_without_bindings
            },
            'templates': self.get_template_statistics(),
            'items': {
                'total': {
                    'all': total_items,
                    'bindable': total_bindable_items,
                    'private': total_private_items,
                },
                'bound': bound_items,
                'unbound': unbound_items
            },
        })

    @staticmethod
    def get_template_statistics():
        """
        Calculates statistics for all items, grouped by their respective templates

        :return: Dict containing a list for every template category with items
        for each existing template and the statistics for its respective items
        """
        template_types = {
            RadioDeviceTemplate: RadioDevice,
            RadioAccessoryTemplate: RadioAccessory,
            PagerTemplate: Pager,
            PhoneTemplate: Phone,
            CallboxTemplate: Callbox,
        }

        res = {}
        for template_type, item_type in template_types.items():
            templates = template_type.objects.annotate(total=Count(item_type.__name__.lower()))

            res[item_type.__name__] = [{
                'pretty_name': tpl.get_pretty_name(),
                'private': tpl.private,
                'total': tpl.total,
                'bound': ItemBinding.objects.filter(**{f'item__{item_type.__name__.lower()}__template': tpl}).count()
            } for tpl in templates]

        return res
