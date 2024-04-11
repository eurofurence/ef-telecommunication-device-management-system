from django.db import models

from .item import Item, ItemTemplate


class RadioCoding(models.Model):
    """
    Model for radio codings.
    """

    name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        help_text="Name of the coding"
    )
    color = models.CharField(
        max_length=7,
        blank=False,
        null=False,
        help_text="Color of the coding in hex format"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the coding"
    )

    def __str__(self):
        return self.name


class RadioDeviceTemplate(ItemTemplate):
    """
    Model for radio templates.
    """

    coding = models.ForeignKey(RadioCoding, on_delete=models.PROTECT)

    def get_pretty_name(self):
        return f"{self.name} {self.coding.__str__()} ({self.owner.shortname})"

    def __str__(self):
        return f"{self.name} {self.coding.__str__()} ({self.owner.shortname}) #{self.pk}"


class RadioDevice(Item):
    """
    Model for radios.
    """

    template = models.ForeignKey(RadioDeviceTemplate, on_delete=models.PROTECT)
    callsign = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="Callsign of the radio"
    )

    def get_pretty_name(self):
        return f"{self.template.name} {self.template.coding.__str__()} ({self.template.owner.shortname}) (CS: {self.callsign}) #{self.pk}"


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

    template = models.ForeignKey(RadioAccessoryTemplate, on_delete=models.PROTECT)

    def get_pretty_name(self):
        return f"{self.template.name} ({self.template.owner.shortname}) #{self.pk}"


class PagerTemplate(ItemTemplate):
    """
    Model for radio pager templates.
    """


class Pager(Item):
    """
    Model for radio pagers.
    """

    template = models.ForeignKey(PagerTemplate, on_delete=models.PROTECT)

    def get_pretty_name(self):
        return f"{self.template.name} ({self.template.owner.shortname}) #{self.pk}"
