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

from rest_framework import serializers


class ObjectWithIdExistsValidator:
    """
    Validator that checks if an object of type model with the given ID exists in the database.
    """

    def __init__(self, model):
        self.model = model

    def __call__(self, value):
        if not self.model.objects.filter(pk=value).exists():
            message = f'No {self.model.__name__} with ID {value} exists.'
            raise serializers.ValidationError(message)
