from django.db import models

from backend.models.user import User


class EventLogEntry(models.Model):
    """
    Model that represents a single event log entry.
    """

    class Action(models.TextChoices):
        USER_LOGIN = 'USER_LOGIN', 'User logged in'
        CREATE_ITEM = 'CREATE_ITEM', 'Item created'
        DELETE_ITEM = 'DELETE_ITEM', 'Item deleted'
        UPDATE_ITEM = 'UPDATE_ITEM', 'Item updated'
        CREATE_ITEM_TEMPLATE = 'CREATE_ITEM_TEMPLATE', 'Item template created'
        DELETE_ITEM_TEMPLATE = 'DELETE_ITEM_TEMPLATE', 'Item template deleted'
        UPDATE_ITEM_TEMPLATE = 'UPDATE_ITEM_TEMPLATE', 'Item template updated'
        CREATE_ITEM_BINDING = 'CREATE_ITEM_BINDING', 'Item binding created'
        DELETE_ITEM_BINDING = 'DELETE_ITEM_BINDING', 'Item binding deleted'

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
