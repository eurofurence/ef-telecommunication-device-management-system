from django.db import models
from polymorphic.models import PolymorphicModel

from backend.models.user import User, ItemOwner


class ItemTemplate(models.Model):
    """
    Model for item templates (e.g., radio device templates)
    """

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


class Item(PolymorphicModel):
    """
    Model for all items (e.g., radios, accessories, telephones, ...)
    """

    template = models.ForeignKey(ItemTemplate, on_delete=models.PROTECT)
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
    handed_out = models.BooleanField(
        blank=False,
        null=False,
        default=False,
        help_text="Whether the item is currently handed out"
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
