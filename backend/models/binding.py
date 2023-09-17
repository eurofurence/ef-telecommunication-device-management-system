from django.db import models

from backend.models.item import Item
from backend.models.user import User


class ItemBinding(models.Model):
    """
    Binding of an item to a user.
    """

    item = models.ForeignKey(
        Item,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text="Item that is bound"
    )
    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        help_text="User that the item is bound to"
    )
    bound_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
        help_text="Date and time when the item was bound"
    )
    bound_by = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="+",
        help_text="User that bound the item"
    )