"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

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
def item_binding_post_save(instance, created, **kwargs):
    """
    Post-save signal receiver for ItemBinding model.

    :param instance: The saved model instance
    :param created: True if the instance was created right now, False on update
    :param kwargs: Additional arguments
    :return: None
    """
    if kwargs.get("raw", False):
        return

    if created:
        action = EventLogEntry.Action.CREATE_ITEM_BINDING
    else:
        action = EventLogEntry.Action.UPDATE_ITEM_BINDING

    EventLogEntry.log(get_current_user(), action, {
        "id": instance.id,
        "item": {
            "id": instance.item.id,
            "pretty_name": instance.item.get_pretty_name(),
        },
        "user": {
            "id": instance.user.id,
            "pretty_name": instance.user.get_pretty_name(),
        }
    })


@receiver(post_delete, sender=ItemBinding, dispatch_uid="item_binding_post_delete")
def item_binding_post_delete(instance, **kwargs):
    """
    Post-delete signal receiver for ItemBinding model.

    :param instance: The deleted model instance
    :param kwargs: Additional arguments
    :return: None
    """
    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_ITEM_BINDING, {
        "id": instance.id,
        "item": {
            "id": instance.item.id,
            "pretty_name": instance.item.get_pretty_name(),
        },
        "user": {
            "id": instance.user.id,
            "pretty_name": instance.user.get_pretty_name(),
        }
    })
