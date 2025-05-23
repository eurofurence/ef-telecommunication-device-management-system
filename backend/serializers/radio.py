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

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory, Pager, RadioCoding, \
    PagerTemplate
from backend.serializers import ItemOwnerSerializer
from backend.serializers.itemcoordinates import ItemCoordinatesSerializer
from backend.serializers.mixins import ItemHandedOutSerializationMixin


class RadioCodingSerializer(serializers.ModelSerializer):
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioCoding
        fields = ['id', 'name', 'color', 'description', 'pretty_name']


class RadioCodingSerializerReduced(serializers.ModelSerializer):
    class Meta:
        model = RadioCoding
        fields = ['id', 'name', 'color']


class RadioDeviceTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    coding = RadioCodingSerializerReduced(read_only=True)
    coding_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioCoding.objects.all(), source='coding')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioDeviceTemplate
        fields = [
            'id',
            'name',
            'description',
            'private',
            'owner',
            'owner_id',
            'coding',
            'coding_id',
            'pretty_name'
        ]


class RadioDeviceSerializer(WritableNestedModelSerializer, ItemHandedOutSerializationMixin):
    template = RadioDeviceTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioDeviceTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)
    handed_out = serializers.SerializerMethodField()
    coordinates = ItemCoordinatesSerializer(source='itemcoordinates', required=False, allow_null=True, many=False)

    class Meta:
        model = RadioDevice
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
            'callsign',
            'coordinates',
        ]


class RadioAccessoryTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessoryTemplate
        fields = [
            'id',
            'name',
            'description',
            'private',
            'owner',
            'owner_id',
            'allow_quickadd',
            'compatible_with',
            'pretty_name'
        ]


class RadioAccessoryTemplateQuickAddSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()
    statistics = serializers.SerializerMethodField()
    type = serializers.ReadOnlyField(default='RadioAccessoryTemplate')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessoryTemplate
        fields = [
            'id',
            'type',
            'name',
            'pretty_name',
            'description',
            'private',
            'owner',
            'allow_quickadd',
            'compatible_with',
            'statistics'
        ]

    def get_statistics(self, obj):
        total = RadioAccessory.objects.filter(template_id=obj.id).count()
        handed_out = RadioAccessory.objects.filter(template_id=obj.id, itembinding__isnull=False).count()
        return {
            'total': total,
            'handed_out': handed_out,
            'available': total - handed_out
        }


class RadioAccessorySerializer(serializers.ModelSerializer, ItemHandedOutSerializationMixin):
    template = RadioAccessoryTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=RadioAccessoryTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)
    handed_out = serializers.SerializerMethodField()

    class Meta:
        model = RadioAccessory
        fields = [
            'id',
            'pretty_name',
            'template',
            'template_id',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]


class PagerTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=ItemOwnerSerializer.Meta.model.objects.all(), source='owner')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = PagerTemplate
        fields = [
            'id',
            'name',
            'description',
            'private',
            'owner',
            'owner_id',
            'pretty_name'
        ]


class PagerSerializer(WritableNestedModelSerializer, ItemHandedOutSerializationMixin):
    template = PagerTemplateSerializer(read_only=True)
    template_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PagerTemplate.objects.all(), source='template')
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)
    handed_out = serializers.SerializerMethodField()
    coordinates = ItemCoordinatesSerializer(source='itemcoordinates', required=False, allow_null=True, many=False)

    class Meta:
        model = Pager
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
            'coordinates',
        ]
