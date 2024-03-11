from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from backend.models import Item
from backend.models import User
from backend.models import EventLogEntry
from backend.models import ItemTemplate


class Order(models.Model):
    """
    (Pre-)Order of a user.
    """

    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text="User that should receive the item"
    )
    title = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Title of the order"
    )
    item = models.ForeignKey(
        Item,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Exact Item that was ordered"
    )
    item_template = models.ForeignKey(
        ItemTemplate,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Exact Item template that was ordered"
    )

    def __str__(self):
        return f"{self.title} for {self.user}"


@receiver(post_save, sender=Order, dispatch_uid="order_post_save")
def order_post_save(instance, created, **kwargs):
    """
    Post-save signal receiver for Order model.

    :param instance: The saved model instance
    :param created: True if the instance was created right now, False on update
    :param kwargs: Additional arguments
    :return: None
    """
    if created:
        action = EventLogEntry.Action.CREATE_ORDER
    else:
        action = EventLogEntry.Action.UPDATE_ORDER

    EventLogEntry.log(instance.bound_by, action, {
        "id": instance.id,
        "user": {
            "id": instance.user.id,
            "pretty_name": instance.user.get_pretty_name(),
        },
        "title": instance.title,
    })


@receiver(post_delete, sender=Order, dispatch_uid="order_post_delete")
def item_binding_post_delete(instance, **kwargs):
    """
    Post-delete signal receiver for Order model.

    :param instance: The deleted model instance
    :param kwargs: Additional arguments
    :return: None
    """
    EventLogEntry.log(instance.bound_by, EventLogEntry.Action.DELETE_ORDER, {
        "id": instance.id,
        "user": {
            "id": instance.user.id,
            "pretty_name": instance.user.get_pretty_name(),
        },
        "title": instance.title,
    })
