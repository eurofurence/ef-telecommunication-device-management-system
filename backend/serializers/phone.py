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
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from backend.models import PhoneTemplate, Phone
from backend.serializers import ItemOwnerSerializer
from backend.serializers.itemcoordinates import ItemCoordinatesSerializer
from backend.serializers.mixins import ItemHandedOutSerializationMixin


class PhoneTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = PhoneTemplate
        fields = ['id', 'name', 'description', 'owner', 'owner_id', 'private', 'pretty_name']


class PhoneSerializer(WritableNestedModelSerializer, ItemHandedOutSerializationMixin):
    template = PhoneTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PhoneTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)
    handed_out = serializers.SerializerMethodField()
    coordinates = ItemCoordinatesSerializer(source='itemcoordinates', required=False, allow_null=True, many=False)

    class Meta:
        model = Phone
        fields = [
            'id',
            'pretty_name',
            'template',
            'template_id',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at',
            'extension',
            'network',
            'dhcp',
            'ip_address',
            'mac_address',
            'location',
            'coordinates',
        ]
