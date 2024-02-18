from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
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

    def __str__(self):
        return f"{self.name} ({self.owner.shortname}) #{self.pk}"


class Item(PolymorphicModel):
    """
    Model for all items (e.g., radios, accessories, telephones, ...)
    """

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

    def __str__(self):
        return f"{self.template.name} ({self.template.owner.shortname}) #{self.pk}"
