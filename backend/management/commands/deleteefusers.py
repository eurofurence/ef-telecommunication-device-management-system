"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

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

from backend.models import User


class Command(BaseCommand):
    help = "Deletes all users that have an EF reg ID assigned but are neither staff nor superuser."

    def handle(self, *args, **options):
        # Fetch all users that are not staff or superuser
        users_to_delete = User.objects.filter(
            is_staff=False,
            is_superuser=False,
            ef_reg_id__isnull=False
        )
        count = users_to_delete.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No EF non staff / superuser accounts found.'))
            return

        # Delete the users
        users_to_delete.delete()

        # Output the result
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} users.'))
