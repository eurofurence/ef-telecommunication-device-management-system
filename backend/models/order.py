"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_currentuser.middleware import get_current_user

from backend.models import Item
from backend.models import User
from backend.models import EventLogEntry
from backend.models import ItemTemplate


class Order(models.Model):
    """
    (Pre-)Order of a user.
    """

    class OrderTypes(models.TextChoices):
        RadioDevice = 'RadioDevice', 'Radio Device'
        RadioAccessory = 'RadioAccessory', 'Radio Accessory'
        Pager = 'Pager', 'Pager'
        Phone = 'Phone', 'Phone'
        Callbox = 'Callbox', 'Callbox'
        Other = 'Other', 'Other'

    user = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        help_text="User that should receive the item"
    )
    type = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        choices=OrderTypes.choices,
        help_text="Type of the order"
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
    if kwargs.get("raw", False):
        return

    if created:
        action = EventLogEntry.Action.CREATE_ORDER
    else:
        action = EventLogEntry.Action.UPDATE_ORDER

    EventLogEntry.log(get_current_user(), action, {
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
    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_ORDER, {
        "id": instance.id,
        "user": {
            "id": instance.user.id,
            "pretty_name": instance.user.get_pretty_name(),
        },
        "title": instance.title,
    })
