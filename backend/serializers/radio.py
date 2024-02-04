from rest_framework import serializers

from backend.models import RadioDeviceTemplate, RadioDevice, RadioAccessoryTemplate, RadioAccessory, Pager
from backend.serializers import ItemOwnerSerializer


class RadioDeviceTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioDeviceTemplate
        fields = ['id', 'name', 'description', 'owner']


class RadioDeviceSerializer(serializers.ModelSerializer):
    template = RadioDeviceTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioDevice
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at',
            'callsign',
        ]


class RadioAccessoryTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner', 'allow_quickadd']


class RadioAccessorySerializer(serializers.ModelSerializer):
    template = RadioAccessoryTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = RadioAccessory
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]


class PagerTemplateSerializer(serializers.ModelSerializer):
    owner = ItemOwnerSerializer()

    class Meta:
        model = RadioAccessoryTemplate
        fields = ['id', 'name', 'description', 'owner']


class PagerSerializer(serializers.ModelSerializer):
    template = PagerTemplateSerializer()
    pretty_name = serializers.CharField(source='get_pretty_name', read_only=True)

    class Meta:
        model = Pager
        fields = [
            'id',
            'pretty_name',
            'template',
            'notes',
            'serialnumber',
            'handed_out',
            'created_at',
            'updated_at'
        ]
