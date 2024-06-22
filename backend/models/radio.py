from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_currentuser.middleware import get_current_user

from . import EventLogEntry
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

    def get_pretty_name(self):
        return f"{self.name} #{self.pk}"

    def __str__(self):
        return self.name


@receiver(post_save, sender=RadioCoding, dispatch_uid="radio_coding_post_save")
def radio_coding_post_save(instance, created, **kwargs):
    """
    Logs creation and update of radio codings.

    :param instance: Saved model instance
    :param created: True if instance was created. False if updated
    :param kwargs: Additional arguments
    :return: None
    """
    if kwargs.get("raw", False):
        return

    if created:
        action = EventLogEntry.Action.CREATE_RADIO_CODING
    else:
        action = EventLogEntry.Action.UPDATE_RADIO_CODING

    EventLogEntry.log(get_current_user(), action, {
        'id': instance.id,
        'name': instance.name,
    })


@receiver(post_delete, sender=RadioCoding, dispatch_uid="radio_coding_post_delete")
def radio_coding_post_delete(instance, **kwargs):
    """
    Logs deletion of radio codings.

    :param instance: Saved model instance
    :param kwargs: Additional arguments
    :return: None
    """
    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_RADIO_CODING, {
        'id': instance.id,
        'name': instance.name,
    })


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
    compatible_with = models.ManyToManyField(
        ItemTemplate,
        related_name='+',
        blank=True,
        help_text="Item templates this accessory is compatible with",
    )


class RadioAccessory(Item):
    """
    Model for radio accessories.
    """

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

    def get_pretty_name(self):
        return f"{self.template.name} ({self.template.owner.shortname}) #{self.pk}"
