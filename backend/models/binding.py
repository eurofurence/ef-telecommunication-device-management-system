from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from backend.models import Item
from backend.models import User
from backend.models import EventLogEntry


class ItemBinding(models.Model):
    """
    Binding of an item to a user.
    """

    item = models.OneToOneField(
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


@receiver(post_save, sender=ItemBinding, dispatch_uid="item_binding_post_save")
def post_save_receiver(instance, created, update_fields, **kwargs):
    """
    Post-save signal receiver for ItemBinding model.

    :param instance: The saved model instance
    :param created: True if the instance was created right now, False on update
    :param update_fields: Saved fields
    """
    if created:
        EventLogEntry.log(instance.bound_by, EventLogEntry.Action.CREATE_ITEM_BINDING, {
            "id": instance.id,
            "item": {
                "pretty_name": instance.item.get_pretty_name(),
            },
            "user": {
                "pretty_name": instance.user.get_pretty_name(),
            }
        })
    else:
        EventLogEntry.log(instance.bound_by, EventLogEntry.Action.UPDATE_ITEM_BINDING, {
            "id": instance.id,
            **update_fields
        })


@receiver(post_delete, sender=ItemBinding, dispatch_uid="item_binding_post_delete")
def post_delete_receiver(instance, **kwargs):
    """
    Post-delete signal receiver for ItemBinding model.

    :param instance: The deleted model instance
    """
    EventLogEntry.log(instance.bound_by, EventLogEntry.Action.DELETE_ITEM_BINDING, {
        "id": instance.id,
        "item": {
            "pretty_name": instance.item.get_pretty_name(),
        },
        "user": {
            "pretty_name": instance.user.get_pretty_name(),
        }
    })
