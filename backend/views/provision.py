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

import os

from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.lib.porvision import provision_generate_config_metadata, provision_generate_firmware_metadata, \
    provision_generate_phonebook_metadata, provision_generate_wallpaper_metadata, provision_retrieve_config, \
    provision_retrieve_phonebook
from backend.settings import PROVISION_CONFIG_DIR


class ProvisionMetadataView(views.APIView):
    """
    API endpoint that allows retrieval of phone provisioning files metadata.
    """
    permission_classes = [IsAdminUser]

    def get(self, response):
        # TODO: Cache metadata generation operations
        ret = {
            'config': provision_generate_config_metadata(),
            'firmware': provision_generate_firmware_metadata(),
            'phonebook': provision_generate_phonebook_metadata(),
            'wallpaper': provision_generate_wallpaper_metadata()
        }

        return Response(ret, status=200)


class ProvisionConfigView(views.APIView):
    """
    API endpoint that allows a single phone config to be retrieved
    """
    permission_classes = [IsAdminUser]

    def get(self, request, mac):
        data = provision_retrieve_config(mac)
        if data is not None:
            return Response(data, status=200)
        else:
            return Response(status=404)

class ProvisionPhonebookView(views.APIView):
    """
    API endpoint that allows a single phonebook to be retrieved
    """
    permission_classes = [IsAdminUser]

    def get(self, request, name):
        data = provision_retrieve_phonebook(name)
        if data is not None:
            return Response(data, status=200)
        else:
            return Response(status=404)
