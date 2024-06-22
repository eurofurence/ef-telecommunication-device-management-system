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

from backend.models import User


class EventLogEntry(models.Model):
    """
    Model that represents a single event log entry.
    """

    class Action(models.TextChoices):
        USER_LOGIN = 'USER_LOGIN', 'User logged in'
        CREATE_ITEM_OWNER = 'CREATE_ITEM_OWNER', 'Item owner created'
        DELETE_ITEM_OWNER = 'DELETE_ITEM_OWNER', 'Item owner deleted'
        UPDATE_ITEM_OWNER = 'UPDATE_ITEM_OWNER', 'Item owner updated'
        CREATE_ITEM = 'CREATE_ITEM', 'Item created'
        DELETE_ITEM = 'DELETE_ITEM', 'Item deleted'
        UPDATE_ITEM = 'UPDATE_ITEM', 'Item updated'
        CREATE_ITEM_TEMPLATE = 'CREATE_ITEM_TEMPLATE', 'Item template created'
        DELETE_ITEM_TEMPLATE = 'DELETE_ITEM_TEMPLATE', 'Item template deleted'
        UPDATE_ITEM_TEMPLATE = 'UPDATE_ITEM_TEMPLATE', 'Item template updated'
        CREATE_ITEM_BINDING = 'CREATE_ITEM_BINDING', 'Item binding created'
        DELETE_ITEM_BINDING = 'DELETE_ITEM_BINDING', 'Item binding deleted'
        UPDATE_ITEM_BINDING = 'UPDATE_ITEM_BINDING', 'Item binding updated'
        CREATE_ORDER = 'CREATE_ORDER', 'Order created'
        DELETE_ORDER = 'DELETE_ORDER', 'Order deleted'
        UPDATE_ORDER = 'UPDATE_ORDER', 'Order updated'
        CREATE_RADIO_CODING = 'CREATE_RADIO_CODING', 'Radio coding created'
        DELETE_RADIO_CODING = 'DELETE_RADIO_CODING', 'Radio coding deleted'
        UPDATE_RADIO_CODING = 'UPDATE_RADIO_CODING', 'Radio coding updated'

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
        help_text="Timestamp of the event"
    )
    action = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        choices=Action.choices,
        help_text="Action that was performed"
    )
    data = models.JSONField(
        blank=True,
        null=True,
        default=None,
        help_text="Additional data optionally associated with the event"
    )

    @classmethod
    def log(cls, user, action, data=None):
        """
        Logs an event.

        :param user: User that performed the action
        :param action: Action that was performed
        :param data: Additional data optionally associated with the event
        """
        cls.objects.create(user=user, action=action, data=data)
