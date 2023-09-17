from django.db import models

from backend.models.user import User


class EventLogEntry(models.Model):
    """
    Model that represents a single event log entry.
    """

    class Action(models.TextChoices):
        USER_LOGIN = 'USER_LOGIN', 'User logged in'

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
