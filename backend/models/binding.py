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

    def __str__(self):
        return f"{self.item} to {self.user} (by {self.bound_by})"

    @classmethod
    def count_users_with_bindings(cls):
        """
        Count the number of users with at least one binding.
        :return: Number of users with at least one binding
        """
        return cls.objects.values('user').distinct().count()
