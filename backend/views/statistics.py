from rest_framework import views
from rest_framework.response import Response

from backend.models import ItemBinding, User, RadioDeviceTemplate, RadioDevice, RadioAccessory, \
    RadioAccessoryTemplate, Pager, PagerTemplate, PhoneTemplate, Phone, CallboxTemplate, Callbox
from backend.permissions import FullDjangoModelPermissions


class StatisticsView(views.APIView):
    """
    API endpoint that returns statistics about ItemBindings
    """

    TEMPLATE_TYPES = {
        RadioDeviceTemplate: RadioDevice,
        RadioAccessoryTemplate: RadioAccessory,
        PagerTemplate: Pager,
        PhoneTemplate: Phone,
        CallboxTemplate: Callbox,
    }

    permission_classes = [FullDjangoModelPermissions]
    queryset = ItemBinding.objects.all()  # Only used for permission check

    def get(self, request, *args, **kwargs):
        total_users = User.objects.count()
        users_with_bindings = ItemBinding.count_users_with_bindings()
        users_without_bindings = total_users - users_with_bindings

        return Response({
            'users': {
                'total': total_users,
                'with_bindings': users_with_bindings,
                'without_bindings': users_without_bindings
            },
            **self.get_item_statistics(),
        })

    @staticmethod
    def get_item_statistics():
        """
        Calculates statistics for all items, grouped by their respective templates

        :return: Dict containing numerical stats for items and a list of templates
        for every item type with entries for each existing template and the
        statistics for its respective template items
        """
        # Prepare result structure
        res = {
            'items': {
                'total': 0,
                'templates': 0,
                'private': 0,
                'bound': 0,
            },
            'templates': {}
        }

        # Iterate over each item type
        for template_type, item_type in StatisticsView.TEMPLATE_TYPES.items():
            templates = template_type.objects.all()

            # Iterate over all existing templates for current item type
            res['templates'][item_type.__name__] = []
            for tpl in templates:
                total = item_type.objects.filter(template=tpl).count()
                bound = ItemBinding.objects.filter(**{f'item__{item_type.__name__.lower()}__template': tpl}).count()

                # Template data
                res['templates'][item_type.__name__].append({
                    'pretty_name': tpl.get_pretty_name(),
                    'private': tpl.private,
                    'total': total,
                    'bound': bound
                })

                # Update global item stats
                res['items']['templates'] += 1
                res['items']['total'] += total
                res['items']['private'] += total if tpl.private else 0
                res['items']['bound'] += bound

        return res
