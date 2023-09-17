from django.db import models

from .item import Item, ItemTemplate


class RadioDeviceTemplate(ItemTemplate):
    """
    Model for radio templates.
    """


class RadioDevice(Item):
    """
    Model for radios.
    """

    callsign = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Callsign of the radio"
    )


class RadioAccessoryTemplate(ItemTemplate):
    """
    Model for radio accessory templates.
    """

    allow_quickadd = models.BooleanField(
        blank=False,
        null=False,
        help_text="Whether to allow quick-adding accessories of this type",
    )


class RadioAccessory(Item):
    """
    Model for radio accessories.
    """
