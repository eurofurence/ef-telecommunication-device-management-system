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

from django.db import models

from backend.models import ItemTemplate, Item


class CallboxTemplate(ItemTemplate):
    """
    Model for security callbox templates.
    """


class Callbox(Item):
    """
    Model for security callboxes.
    """

    class Network(models.TextChoices):
        STAFF = 'STAFF', 'Staff'
        SECU = 'SECU', 'Security'

    extension = models.CharField(
        max_length=32,
        blank=False,
        null=False,
        help_text="Extension (e.g., call number) of the phone"
    )
    network = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        choices=Network.choices,
        help_text="Network the phone is on"
    )
    dhcp = models.BooleanField(
        blank=False,
        null=False,
        help_text="Whether the phone uses DHCP"
    )
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="IP address of the phone, if static"
    )
    mac_address = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        help_text="MAC address of the phone"
    )
    location = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="Location of the phone"
    )
    has_camera = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        help_text="Whether the callbox has a camera"
    )
    camera_network = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        choices=Network.choices,
        help_text="Network the camera is on"
    )
    camera_dhcp = models.BooleanField(
        blank=True,
        null=True,
        help_text="Whether the camera uses DHCP"
    )
    camera_ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="IP address of the camera"
    )
    camera_mac_address = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        help_text="MAC address of the camera"
    )

    def get_pretty_name(self):
        return f"{self.template.name} {self.location} (EXT: {self.extension}) #{self.pk}"
