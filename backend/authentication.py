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
