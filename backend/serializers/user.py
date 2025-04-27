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

from rest_framework import serializers

from backend.models import User, ItemOwner


class UserSerializer(serializers.ModelSerializer):
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nickname', 'pretty_name', 'email', 'ef_reg_id', 'ef_security_collar_id', 'last_login']


class ItemOwnerSerializer(serializers.ModelSerializer):
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = ItemOwner
        fields = ['id', 'name', 'shortname', 'pretty_name']
