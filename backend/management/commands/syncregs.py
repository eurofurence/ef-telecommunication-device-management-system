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
import re
import urllib.parse

from django.core.management.base import BaseCommand

import requests

from backend.models import User


class Command(BaseCommand):

    help = "Synchronizes the local user database with the Eurofurence Registration System."
    """ Help text for the command. """

    PAGESIZE = 500
    """ Number of attendees to fetch per page. """

    API_ENDPOINT = "attendees/find"
    """ API endpoint to fetch attendees. """

    def add_arguments(self, parser):
        """
        Add command line arguments to the command.

        :param parser:
        :return:
        """
        parser.add_argument(
            'API_BASE_URL',
            type=str,
            help='The base URL of the current Eurofurence Registration System API (e.g., https://reglive.eurofurence.org/20240114-1459-r3v1/attsrv/api/rest/v1/).'
        )
        parser.add_argument(
            'JWT',
            type=str,
            help='The JSON Web Token (JWT) to authenticate against the Eurofurence Registration System API.'
        )
        parser.add_argument('--force',
            action='store_true',
            default=False,
            help='Force synchronization, even if a conflicting user entry is found locally.'
        )

    def handle(self, *args, **options):
        """
        Main entrance point for command execution (called by Djangos manage.py).

        :param args:
        :param options:
        :return:
        """
        self.stdout.write("Synchronizing user database with Eurofurence Registration System...")
        self.stdout.write(f" -> API Base URL: {options['API_BASE_URL']}")
        self.stdout.write("")

        # Get regs from API and update local user database
        page_idx = 0
        processed_users = 0
        created_or_updated_users = 0
        while True:
            # Get attendees page
            attendees = self._get_attendees_page(options['API_BASE_URL'], options['JWT'], page_idx)

            # Check if there are any attendees left
            if len(attendees) == 0:
                break

            # Process attendees
            for attendee in attendees:
                created_or_updated = self._update_user(
                    efregid=attendee['id'],
                    nickname=attendee['nickname'],
                    first_name=attendee['first_name'],
                    last_name=attendee['last_name'],
                    force=options['force']
                )
                processed_users += 1
                if created_or_updated:
                    created_or_updated_users += 1

            # Continue with next page
            page_idx += 1

        self.stdout.write(f"\nSynchronization completed.")
        self.stdout.write(f"  -> Processed: {processed_users}")
        self.stdout.write(f"  -> Created or updated: {created_or_updated_users}")

    def _get_attendees_page(self, api_base_url: str, jwt: str, page: int) -> list:
        """
        Retrieves a page of attendees from the Eurofurence Registration System API.

        :param api_base_url: Base URL of the regsys API
        :param jwt: JSON Web Token to authenticate against the API
        :param page: Page index
        :return: List of attendees for the requested page
        """
        # Send API request
        apiurl = urllib.parse.urljoin(api_base_url, self.API_ENDPOINT)
        r = requests.post(
            url=apiurl,
            headers={
                "Cookie": f"JWT={jwt}"
            },
            json={
                "match_any": [
                    {
                        "nickname": "*"
                    }
                ],
                "fill_fields": [
                    "id",
                    "nickname",
                    "first_name",
                    "last_name",
                ],
                "min_id": page * self.PAGESIZE,
                "max_id": (page + 1) * self.PAGESIZE,
                "sort_by": "id",
                "sort_order": "ascending"
            }
        )

        # Check status
        if r.status_code != 200:
            raise Exception(f"Request to {apiurl} for page {page} failed with status code HTTP {r.status_code}")

        data = r.json()
        if 'attendees' not in data:
            raise Exception(f"Request for page {page} did not return any attendees: {data}")

        return data['attendees']

    def _update_user(self, efregid: int, nickname: str, first_name: str, last_name: str, force: bool = False) -> bool:
        """
        Updates a local user record. Creates user if not found. Updates only if force is set to True.

        :param efregid: Eurofurence registration ID of the user
        :param nickname: Nickname of the user
        :param first_name: First name of the user
        :param last_name:  Last name of the user
        :param force: If True, updates existing user records even if they are conflicting
        :return: True, if the user was created or updated. False, if the user was not updated.
        """
        # Try to get user
        try:
            user = User.objects.get(ef_reg_id=efregid)
        except User.DoesNotExist:
            user = None

        if user is None:
            # Create new user
            user = User(
                username=self._generate_username(efregid, nickname),
                ef_reg_id=efregid,
                nickname=nickname,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            self.stdout.write(f"Created user: #{efregid} {nickname} ({first_name} {last_name}) with username '{user.username}'")
            return True
        else:
            # Check if existing user record matches the new data
            if (user.nickname == nickname and
                user.first_name == first_name and
                user.last_name == last_name):
                return False
            else:
                if not force:
                    self.stderr.write(f"[ERROR] Skipping conflicting user:")
                    self.stderr.write(f"  -> Existing: #{user.ef_reg_id} {user.nickname} ({user.first_name} {user.last_name})")
                    self.stderr.write(f"  ->      New: #{efregid} {nickname} ({first_name} {last_name})")
                    return False
                else:
                    # Update user
                    user.nickname = nickname
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    self.stdout.write(f"[WARN] Updating existing user: #{efregid} {nickname} ({first_name} {last_name})")

    @staticmethod
    def _generate_username(regid: int, nickname: str) -> str:
        """
        Generates a unique username based on the registration ID and nickname.

        :param regid: Eurofurence registration ID
        :param nickname: Nickname
        :return: Unique username
        """
        cleannick = re.sub(r'[^a-zA-Z0-9]', '', nickname).lower()
        cleannick = (cleannick[:64] if len(cleannick) > 64 else cleannick)

        return f"{regid}_{cleannick}"