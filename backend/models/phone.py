from django.db import models

from backend.models import ItemTemplate, Item


class PhoneTemplate(ItemTemplate):
    """
    Model for phone templates.
    """


class Phone(Item):
    """
    Model for phones.
    """
    class Network(models.TextChoices):
        STAFF = 'STAFF', 'Staff'
        SECU = 'SECU', 'Security'

    template = models.ForeignKey(PhoneTemplate, on_delete=models.PROTECT)
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
