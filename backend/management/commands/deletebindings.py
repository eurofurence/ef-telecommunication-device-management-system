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

from backend.models import ItemBinding


class Command(BaseCommand):
    help = "Deletes all existing item bindings."

    def handle(self, *args, **options):
        # Fetch all item bindings
        bindings_to_delete = ItemBinding.objects.all()
        count = bindings_to_delete.count()
        if count == 0:
            self.stdout.write(self.style.WARNING('No item bindings found.'))
            return

        # Delete the item bindings
        bindings_to_delete.delete()

        # Output the result
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} item bindings.'))
