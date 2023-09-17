from django.db import models

from backend.models.phone import PhoneTemplate, Phone


class CallboxTemplate(PhoneTemplate):
    """
    Model for security callbox templates.
    """


class Callbox(Phone):
    """
    Model for security callboxes.
    """

    has_camera = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        help_text="Whether the callbox has a camera"
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
