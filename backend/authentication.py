from typing import TypeVar
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.authentication import TokenUser

AuthUser = TypeVar('AuthUser', AbstractBaseUser, TokenUser)


def simplejwt_user_authentication_rule(user: AuthUser) -> bool:
    """
    Custom user authentication rule for SimpleJWT. This rule only allows valid
    users that are active and have the is_staff flag assigned to authenticate.

    :param user: The user to check
    :return: True if the user is valid, False otherwise
    """
    return user is not None and user.is_active and user.is_staff
