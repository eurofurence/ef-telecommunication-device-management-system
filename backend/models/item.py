from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django_currentuser.middleware import get_current_user
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from polymorphic.models import PolymorphicModel

from backend.models.user import User, ItemOwner
from backend.models import EventLogEntry


class ItemTemplate(PolymorphicModel):
    """
    Model for item templates (e.g., radio device templates)
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        post_save.connect(item_template_post_save, sender=cls)
        post_delete.connect(item_template_post_delete, sender=cls)

    name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Name of the item this template is for"
    )
    description = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default=None,
        help_text="Description of the item this template is for"
    )
    owner = models.ForeignKey(
        ItemOwner,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text="User that owns the items that use this template"
    )
    private = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text="Whether this items are private and should not be issued via this system"
    )

    def get_pretty_name(self):
        return f"{self.name} ({self.owner.shortname})"

    def __str__(self):
        return f"{self.name} ({self.owner.shortname}) #{self.pk}"


@receiver(post_save, sender=ItemTemplate, dispatch_uid="item_template_post_save")
def item_template_post_save(instance, created, **kwargs):
    """
    Logs creation and update of item templates.

    :param instance: Saved model instance
    :param created: True if instance was created. False if updated
    :param kwargs: Additional arguments
    :return: None
    """
    if kwargs.get("raw", False):
        return

    # Do not log operations on polymorphic base classes
    if type(instance) is ItemTemplate:
        return

    if created:
        action = EventLogEntry.Action.CREATE_ITEM_TEMPLATE
    else:
        action = EventLogEntry.Action.UPDATE_ITEM_TEMPLATE

    EventLogEntry.log(get_current_user(), action, {
        'id': instance.id,
        'pretty_name': instance.get_pretty_name(),
        'name': instance.name,
        'owner': model_to_dict(instance.owner, fields=['name', 'shortname'])
    })


@receiver(post_delete, sender=ItemTemplate, dispatch_uid="item_template_post_delete")
def item_template_post_delete(instance, **kwargs):
    """
    Logs deletion of item templates.

    :param instance: Saved model instance
    :param kwargs: Additional arguments
    :return: None
    """
    # Do not log operations on polymorphic base classes
    if type(instance) is ItemTemplate:
        return

    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_ITEM_TEMPLATE, {
        'id': instance.id,
        'pretty_name': instance.get_pretty_name(),
        'name': instance.name,
        'owner': model_to_dict(instance.owner, fields=['name', 'shortname'])
    })


class ItemCoordinates(models.Model):
    """
    Model for item coordinates on the deployment map
    """

    item = models.OneToOneField(
        'Item',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text="Item this location is for"
    )
    floor = models.IntegerField(
        blank=False,
        null=False,
        help_text="Floor number of the item location"
    )
    latitude = models.FloatField(
        blank=False,
        null=False,
        help_text="Latitude of the item location"
    )
    longitude = models.FloatField(
        blank=False,
        null=False,
        help_text="Longitude of the item location"
    )


class Item(PolymorphicModel):
    """
    Model for all items (e.g., radios, accessories, telephones, ...)
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        post_save.connect(item_post_save, sender=cls)
        post_delete.connect(item_post_delete, sender=cls)

    template = models.ForeignKey(
        ItemTemplate,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text="Template this item is based on"
    )
    notes = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        default=None,
        help_text="Optional notes about the item"
    )
    serialnumber = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        default=None,
        help_text="Optional serial number of the item"
    )
    created_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
        help_text="Date and time when the item was created"
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="User that created the item"
    )
    updated_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
        help_text="Date and time when the item was last updated"
    )

    @extend_schema_field(OpenApiTypes.BOOL)
    def handed_out(self):
        from backend.models import ItemBinding

        return ItemBinding.objects.filter(item=self).exists()

    def get_pretty_name(self):
        if self.__class__.__name__ == "Item":
            return f"Item Base #{self.pk}"
        else:
            return f"{self.template.name} ({self.template.owner.shortname})"

    def __str__(self):
        if self.__class__.__name__ == "Item":
            return f"Item Base #{self.pk}"
        else:
            return f"{self.template.name} ({self.template.owner.shortname}) #{self.pk}"


@receiver(post_save, sender=Item, dispatch_uid="item_post_save")
def item_post_save(instance, created, **kwargs):
    """
    Logs creation and update of item templates.

    :param instance: Saved model instance
    :param created: True if instance was created. False if updated
    :param kwargs: Additional arguments
    :return: None
    """
    if kwargs.get("raw", False):
        return

    # Do not log operations on polymorphic base classes
    if type(instance) is Item:
        return

    if created:
        action = EventLogEntry.Action.CREATE_ITEM
    else:
        action = EventLogEntry.Action.UPDATE_ITEM

    EventLogEntry.log(get_current_user(), action, {
        'id': instance.id,
        'pretty_name': instance.get_pretty_name()
    })


@receiver(post_delete, sender=Item, dispatch_uid="item_post_delete")
def item_post_delete(instance, **kwargs):
    """
    Logs deletion of items.

    :param instance: Saved model instance
    :param kwargs: Additional arguments
    :return: None
    """
    # Do not log operations on polymorphic base classes
    if type(instance) is Item:
        return

    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_ITEM, {
        'id': instance.id,
        'pretty_name': instance.get_pretty_name()
    })
