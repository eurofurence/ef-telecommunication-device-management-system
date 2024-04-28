from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class BackendConfig(AppConfig):
    name = 'backend'
    verbose_name = 'Backend'


@receiver(post_migrate, dispatch_uid="backend_post_migrate")
def backend_post_migrate(sender, **kwargs):
    """
    Post-migrate signal receiver for backend app.

    :param sender: The sender of the signal
    :param kwargs: Additional keyword arguments
    :return: None
    """
    if sender.name != BackendConfig.name:
        return

    from django.contrib.auth.models import Group, Permission

    # Setup default permission group ManagerReadOnly
    # This group has read-only access to all models
    print('Setting up default permission groups ...')
    g_managerreadonly, created = Group.objects.get_or_create(name='ManagerReadOnly')
    g_managerreadonly.permissions.clear()
    for perm in Permission.objects.filter(content_type__app_label='backend', codename__startswith='view_'):
        g_managerreadonly.permissions.add(perm)
    print(f"  -> Group 'ManagerReadOnly' has been set up with {g_managerreadonly.permissions.count()} permissions.")

    # Setup default permission group Manager
    # This group has full access to all models except User (read-only)
    g_manager, created = Group.objects.get_or_create(name='Manager')
    g_manager.permissions.clear()
    for perm in Permission.objects.filter(content_type__app_label='backend').exclude(content_type__model='user'):
        g_manager.permissions.add(perm)
    g_manager.permissions.add(Permission.objects.get(codename='view_user'))
    print(f"  -> Group 'Manager' has been set up with {g_manager.permissions.count()} permissions.")
