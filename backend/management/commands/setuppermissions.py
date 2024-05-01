from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Creates and populates or updates the default permission groups."

    def handle(self, *args, **options):
        # Setup default permission group ManagerReadOnly
        # This group has read-only access to all models
        self.stdout.write('Setting up default permission groups ...')
        g_managerreadonly, created = Group.objects.get_or_create(name='ManagerReadOnly')
        g_managerreadonly.permissions.clear()
        for perm in Permission.objects.filter(content_type__app_label='backend', codename__startswith='view_'):
            g_managerreadonly.permissions.add(perm)
        self.stdout.write(f"  -> Group 'ManagerReadOnly' has been set up with {g_managerreadonly.permissions.count()} permissions.")

        # Setup default permission group Manager
        # This group has full access to all models except User (read-only)
        g_manager, created = Group.objects.get_or_create(name='Manager')
        g_manager.permissions.clear()
        for perm in Permission.objects.filter(content_type__app_label='backend').exclude(content_type__model='user'):
            g_manager.permissions.add(perm)
        g_manager.permissions.add(Permission.objects.get(codename='view_user'))
        self.stdout.write(f"  -> Group 'Manager' has been set up with {g_manager.permissions.count()} permissions.")

        self.stdout.write(self.style.SUCCESS('Default permission groups have been set up successfully.'))
