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

from backend.models import Order
from backend.serializers import UserSerializer
from backend.serializers.item import PolymorphicItemSerializer, PolymorphicItemTemplateSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserSerializer.Meta.model.objects.all(), source='user')
    item = PolymorphicItemSerializer(read_only=True)
    # TODO: Implement write support for item
    item_template = PolymorphicItemTemplateSerializer(read_only=True)
    # TODO: Implement write support for item_template
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_id',
            'type',
            'title',
            'item',
            'item_template',
            'pretty_name'
        ]
