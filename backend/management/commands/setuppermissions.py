"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
