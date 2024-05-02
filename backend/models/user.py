from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from django_currentuser.middleware import get_current_user


class User(AbstractUser):
    """
    Extended User model to store additional information about the user.
    """
    nickname = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Nickname of the user"
    )
    ef_reg_id = models.PositiveIntegerField(
        blank=False,
        null=True,
        unique=True,
        help_text="ID of the user in the EF reg database"
    )
    ef_security_collar_id = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=None,
        unique=True,
        help_text="ID of the user in the EF security collar database"
    )
    last_seen = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="Last time the user was seen on the platform"
    )

    def get_pretty_name(self):
        return f"{self.nickname} (Reg-ID: {self.ef_reg_id})"


@receiver(post_save, sender=User, dispatch_uid="user_post_save")
def user_post_save(instance, update_fields, created, **kwargs):
    """
    Logs user logins

    :param instance: The affected user
    :param update_fields: Updated fields
    :param created: True, if user was created during operation. False on update.
    :param kwargs: Additional args
    :return: None
    """
    if kwargs.get("raw", False):
        return

    if update_fields is not None:
        if not created and 'last_login' in update_fields:
            from backend.models import EventLogEntry
            EventLogEntry.log(instance, EventLogEntry.Action.USER_LOGIN)


class ItemOwner(models.Model):
    """
    Represents a person that owns items.
    """

    name = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Name of the owner"
    )
    shortname = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        unique=True,
        help_text="Short name of the owner"
    )

    def get_pretty_name(self):
        return f"{self.name} ({self.shortname})"

    def __str__(self):
        return self.name


@receiver(post_save, sender=ItemOwner, dispatch_uid="item_owner_post_save")
def item_owner_post_save(instance, created, **kwargs):
    """
    Logs the creation and updates of item owners.

    :param instance: The saved model instance
    :param created: True if the instance was created right now, False on update
    :param kwargs: Additional args
    :return: None
    """
    if kwargs.get("raw", False):
        return

    from backend.models import EventLogEntry

    if created:
        action = EventLogEntry.Action.CREATE_ITEM_OWNER
    else:
        action = EventLogEntry.Action.UPDATE_ITEM_OWNER

    EventLogEntry.log(get_current_user(), action, model_to_dict(instance))


@receiver(post_delete, sender=ItemOwner, dispatch_uid="item_owner_post_delete")
def item_owner_post_delete(instance, **kwargs):
    """
    Logs the deletion of item owners.

    :param instance: The deleted model instance
    :param kwargs: Additional args
    :return: None
    """
    from backend.models import EventLogEntry
    EventLogEntry.log(get_current_user(), EventLogEntry.Action.DELETE_ITEM_OWNER, model_to_dict(instance))
