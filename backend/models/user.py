from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Extended User model to store additional information about the user.
    """
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
        return f"{self.username} (Reg-ID: {self.ef_reg_id})"


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
        help_text="Short name of the owner"
    )

    def __str__(self):
        return self.name
